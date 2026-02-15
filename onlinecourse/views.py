from django.shortcuts import render, get_object_or_404, redirect
from .models import Course, Question, Submission, Choice

# ... other views like CourseListView ...

# Function to handle the exam submission
def submit(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    if request.method == 'POST':
        # Extract selected choices from the POST data
        # The HTML checkboxes should have name="choice_{{question.id}}"
        question_ids = [q.id for q in course.question_set.all()]
        selected_choice_ids = []
        for q_id in question_ids:
            selected_ids = request.POST.getlist(f'choice_{q_id}')
            selected_choice_ids.extend([int(sid) for sid in selected_ids])
        
        # Create a new submission object
        submission = Submission()
        submission.enrollment = course.enrollment_set.filter(user=request.user).first()
        submission.save()
        
        # Link selected choices to the submission
        for choice_id in selected_choice_ids:
            choice = get_object_or_404(Choice, pk=choice_id)
            submission.choices.add(choice)
        submission.save()

        return redirect('onlinecourse:show_exam_result', course_id=course.id, submission_id=submission.id)

# Function to calculate and display the result
def show_exam_result(request, course_id, submission_id):
    course = get_object_or_404(Course, pk=course_id)
    submission = get_object_or_404(Submission, pk=submission_id)
    
    # Context to pass to the template
    context = {}
    context['course'] = course
    context['grade'] = submission.calculate_score() # Logic usually defined in models.py
    context['submission'] = submission
    
    return render(request, 'onlinecourse/exam_result_bootstrap.html', context)
