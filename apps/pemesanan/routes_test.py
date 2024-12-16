# @blueprint.route('/test-celery', methods=['GET'])
# def test_celery():
#     task = test_get_montir.delay()
#     return render_template(
#         'pemesanan/test_celery.html',
#         task_id=task.id
#     )

# @blueprint.route('/test-result/<task_id>')
# def test_result(task_id):
#     task = test_get_montir.AsyncResult(task_id)
    
#     if task.state == 'PENDING':
#         return 'Task sedang berjalan...'
#     elif task.state == 'SUCCESS':
#         return f'Hasil: {task.result}'
#     else:
#         return f'Task status: {task.state}, Result: {task.result}'