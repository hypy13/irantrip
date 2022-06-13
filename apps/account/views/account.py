from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated

from ..serializers.account import UserInfoSerializer


class UserInfoView(RetrieveUpdateAPIView):
    serializer_class = UserInfoSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser,)

    def update(self, request, *args, **kwargs):
        if avatar_file := request.FILES.get('avatar'):
            avatar = self.save_image_to_filer(avatar_file, request.user)
            del request.data['avatar']
            request.data['avatar_id'] = avatar.id

        return super(UserInfoView, self).update(request, *args, *kwargs)

    def perform_update(self, serializer):
        if avatar_id := self.request.data.get('avatar_id'):
            serializer.save(avatar_id=avatar_id)

        serializer.save()

    def get_object(self):
        return self.request.user

    def save_image_to_filer(self, file, owner, folder=None, name=None):
        from django.core.files import File
        from filer.models.imagemodels import Image
        if not folder:
            from filer.models.foldermodels import Folder
            folder, created = Folder.objects.get_or_create(defaults={
                'name': 'avatars',
            }, name='avatars')

        image = Image.objects.create(
            owner=owner,
            original_filename=name or file.name,
            file=File(file, name=name or file.name),
            folder=folder,
        )
        return image
