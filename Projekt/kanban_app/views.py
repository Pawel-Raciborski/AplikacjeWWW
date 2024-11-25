from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from tutorial.quickstart.serializers import UserSerializer

from kanban_app.models import Board
from kanban_app.serializers import BoardSerializer


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
