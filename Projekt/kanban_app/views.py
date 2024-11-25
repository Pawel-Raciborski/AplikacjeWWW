from datetime import timedelta

from django.contrib.auth.models import User
from django.utils.timezone import now
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from tutorial.quickstart.serializers import UserSerializer

from kanban_app.models import Board, Column, Task, Comment
from kanban_app.serializers import BoardSerializer, ColumnSerializer, TaskSerializer, CommentSerializer


# Create your views here.

@api_view(['POST'])
def create_board(request):
    if request.method == 'POST':
        data = request.data.copy()
        data['owner'] = request.user.pk
        serializer = BoardSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Utworzono tablicę'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_board(request, pk):
    if request.method == 'GET':
        board = Board.objects.get(pk=pk)
        serializer = BoardSerializer(board)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


@api_view(['PUT', 'PATCH'])
def update_board(request, pk):
    try:
        board = Board.objects.get(pk=pk)
    except Board.DoesNotExist:
        return Response({'message': 'Nie znaleziono'}, status=status.HTTP_404_NOT_FOUND)

    partial = request.method == 'PATCH'
    serializer = BoardSerializer(board, data=request.data, partial=partial)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_all_boards(request):
    if request.user.is_authenticated:
        user_boards = Board.objects.filter(owner=request.user)
        serializer = BoardSerializer(user_boards, many=True)
        return Response(serializer.data)
    else:
        return Response(status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET'])
def get_board_members(request, pk):
    try:
        board = Board.objects.get(pk=pk, owner=request.user)
    except Board.DoesNotExist:
        return Response({'message': 'Nie znaleziono'}, status=status.HTTP_404_NOT_FOUND)

    users = board.users.all()
    serializer = UserSerializer(users, many=True)
    if serializer.is_valid():
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PATCH'])
def add_member_to_board(request, board_id):
    try:
        board = Board.objects.get(pk=board_id)
    except Board.DoesNotExist:
        return Response({"message": "Nie znaleziono podanego projektu"}, status=status.HTTP_404_NOT_FOUND)

    users_to_add_ids = request.data.get('users_ids', [])
    users_to_add = User.objects.filter(id__in=users_to_add_ids)

    if not users_to_add.exists():
        return Response({"error": "Lista jest pusta"}, status=status.HTTP_400_BAD_REQUEST)

    board.users.add(*users_to_add)

    return Response({
        "message": "Dodano nowych użytkowników",
        "board_id": board.id,
        "added_users": [user.id for user in users_to_add],
        "current_users": [user.id for user in board.users.all()]
    })


@api_view(['DELETE'])
def remove_member_from_board(request, board_id):
    try:
        board = Board.objects.get(pk=board_id)
    except Board.DoesNotExist:
        return Response({"message": "Nie znaleziono podanego projektu"}, status=status.HTTP_404_NOT_FOUND)

    users_to_remove_ids = request.data.get('users_ids', [])
    users_to_remove = User.objects.filter(id__in=users_to_remove_ids)

    if not users_to_remove.exists():
        return Response({"error": "Lista jest pusta"}, status=status.HTTP_400_BAD_REQUEST)

    if board.owner in users_to_remove:
        return Response({"error": f"Nie można usunąć właściciela o id:{board.owner.id} z tablicy!"},
                        status=status.HTTP_400_BAD_REQUEST)

    board.users.remove(*users_to_remove)
    return Response(
        {
            'message': 'Użytkownicy usunięci z tablicy pomyślnie',
            'board_id': board.id,
            'removed_users_ids': [user.id for user in users_to_remove],
            'current_users': [user.id for user in board.users.all()]
        },
        status=status.HTTP_200_OK
    )


@api_view(['DELETE'])
def delete_board(request, board_id):
    try:
        board = Board.objects.get(id=board_id)
    except Board.DoesNotExist:
        return Response({"error": f"Nie znaleziono tablicy o id {board_id}"}, status=status.HTTP_404_NOT_FOUND)

    if board.owner != request.user:
        return Response(
            {'error': f"Nie masz uprawnień do usunięcia tej tablicy!"},
            status=status.HTTP_403_FORBIDDEN
        )

    board.delete()

    return Response("Usunięto pomyślnie projekt", status=status.HTTP_200_OK)


@api_view(['GET'])
def get_all_columns(request, board_id):
    try:
        board = Board.objects.get(id=board_id)
    except Board.DoesNotExist:
        return Response({'error': 'Nie znaleziono projektu'}, status=status.HTTP_404_NOT_FOUND)

    columns = board.columns.all().order_by('order')
    serializer = ColumnSerializer(columns, many=True)

    return Response({
        'message': 'Pobrano kolumny projektu',
        'columns': serializer.data
    }, status=status.HTTP_200_OK)


# Column CRUD

@api_view(['POST'])
def create_column(request):
    column_serializer = ColumnSerializer(data=request.data)

    column_exist = Column.objects.filter(board_id=request.data['board'],
                                         order=request.data['order'],
                                         name=request.data['name']).exists()
    if column_exist:
        return Response({
            'message': 'Dla podanej tabeli istneje kolumna o podanej nazwie!'
        }, status=status.HTTP_400_BAD_REQUEST)

    if column_serializer.is_valid():
        column_serializer.save()
        return Response({
            'message': "Utworzono kolumnę",
            'column': column_serializer.data
        },
            status=status.HTTP_201_CREATED
        )
    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT', 'PATCH'])
def update_column(request, column_id):
    try:
        column_to_update = Column.objects.get(pk=column_id)
    except Column.DoesNotExist:
        return Response({'error': 'Nie znaleziono kolumny'}, status=status.HTTP_404_NOT_FOUND)

    partial = request.method == 'PATCH'
    serializer = ColumnSerializer(column_to_update, data=request.data, partial=partial)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def delete_column(request, column_id):
    try:
        column_to_delete = Column.objects.get(pk=column_id)
    except Column.DoesNotExist:
        return Response({'error': 'Nie znaleziono kolumny'}, status=status.HTTP_404_NOT_FOUND)

    column_to_delete.delete()
    return Response({'message': f"Usunięto kolumnę o id {column_id}"}, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_column_tasks(request, column_id):
    try:
        column = Column.objects.get(pk=column_id)
    except Column.DoesNotExist:
        return Response({'error': 'Nie znaleziono kolumny'}, status=status.HTTP_404_NOT_FOUND)

    tasks = column.tasks.all().order_by('due_date')
    serializer = TaskSerializer(tasks, many=True)

    return Response({
        "message": "Pobrano wszystkie zadania podanej kolumny",
        "tasks": serializer.data
    })


@api_view(['POST'])
def create_task(request):
    task_serializer = TaskSerializer(data=request.data)

    if task_serializer.is_valid():
        task_serializer.save()
        return Response({
            'message': "Pomyślnie utworzono zadanie",
            'task': task_serializer.data
        }, status=status.HTTP_201_CREATED)


@api_view(['PUT', 'PATCH'])
def update_task(request, task_id):
    try:
        column_to_update = Task.objects.get(pk=task_id)
    except Task.DoesNotExist:
        return Response({'error': 'Nie znaleziono podanego zadania'}, status=status.HTTP_404_NOT_FOUND)

    partial = request.method == 'PATCH'
    serializer = TaskSerializer(column_to_update, data=request.data, partial=partial)

    if serializer.is_valid():
        serializer.save()
        return Response({
            'message': "Zaktualizowano zadanie",
            'updatedTask': serializer.data
        }, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def delete_task(request, task_id):
    try:
        task_to_delete = Task.objects.get(pk=task_id)
    except Task.DoesNotExist:
        return Response({
            'error': 'Nie znaleziono podanego zadania'
        }, status=status.HTTP_404_NOT_FOUND)

    task_to_delete.delete()

    return Response({'message': f'Usunięto pomyślnie zadanie o id {task_id}'}, status=status.HTTP_200_OK)


@api_view(['PATCH'])
def add_users_to_task(request, task_id):
    try:
        task = Task.objects.get(pk=task_id)
    except Task.DoesNotExist:
        return Response({
            'error': 'Nie znaleziono podanego zadania'
        }, status=status.HTTP_404_NOT_FOUND)

    users_ids = request.data.get('users_ids', [])
    users = User.objects.filter(id__in=users_ids)

    if not users.exists():
        return Response({"error": "Lista jest pusta"}, status=status.HTTP_400_BAD_REQUEST)

    task.assign_users.add(*users)
    return Response({
        "message": "Dodano nowych użytkowników",
        "task_id": task_id,
        "added_users": [user.id for user in users],
        "current_users": [user.id for user in task.assign_users.all()]
    })


@api_view(['DELETE'])
def remove_users_from_task(request, task_id):
    try:
        task = Task.objects.get(pk=task_id)
    except Task.DoesNotExist:
        return Response({
            'error': 'Nie znaleziono podanego zadania'
        }, status=status.HTTP_404_NOT_FOUND)

    users_ids = request.data.get('users_ids', [])
    users = User.objects.filter(id__in=users_ids)

    if not users.exists():
        return Response({"error": "Lista jest pusta"}, status=status.HTTP_400_BAD_REQUEST)

    task.assign_users.remove(*users)
    return Response({
        "message": "Usunięto użytkowników z zadania",
        "task_id": task_id,
        "removed_users": [user.id for user in users],
        "current_users": [user.id for user in task.assign_users.all()]
    })


# CRUD Comment

@api_view(['POST'])
def add_comment(request):
    request_data = request.data.copy()
    request_data['user'] = request.user.pk
    comment_serializer = CommentSerializer(data=request_data)

    if comment_serializer.is_valid():
        comment_serializer.save()
        return Response({
            'message': "Pomyślnie utworzono komentarz",
            'comment': comment_serializer.data
        }, status=status.HTTP_201_CREATED)
    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['PATCH'])
def edit_comment(request, comment_id):
    try:
        comment_to_update = Comment.objects.get(pk=comment_id)
    except Comment.DoesNotExist:
        return Response({
            'error': "Nie znaleziono komentarza!"
        }, status=status.HTTP_404_NOT_FOUND)

    time_edit_limit = comment_to_update.created_at + timedelta(minutes=10)

    if now() > time_edit_limit:
        return Response({
            'error': 'Upłynął czas umożliwiający edycję komentarza!'
        }, status=status.HTTP_409_CONFLICT)

    serializer = CommentSerializer(comment_to_update, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def remove_comment(request, comment_id):
    try:
        comment_to_delete = Comment.objects.get(pk=comment_id)
    except Comment.DoesNotExist:
        return Response({
            'error': "Nie znaleziono komentarza!"
        }, status=status.HTTP_404_NOT_FOUND)

    comment_to_delete.delete()
    return Response({
        'message': 'Komentarz usunięto pomyślnie'
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_task_comments(request, task_id):
    try:
        task = Task.objects.get(pk=task_id)
    except Task.DoesNotExist:
        return Response({
            'error': 'Nie znaleziono podanego zadania'
        }, status=status.HTTP_404_NOT_FOUND)

    task_comments = task.comments.all()
    serializer = CommentSerializer(task_comments, many=True)

    return Response({
        'message': 'Lista komentarzy',
        'comments': serializer.data
    }, status=status.HTTP_200_OK)
