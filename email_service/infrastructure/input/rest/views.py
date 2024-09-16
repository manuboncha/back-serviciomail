import inject
from django.urls import reverse
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from email_service.application.use_case.find_email_use_case_impl import FindEmailUseCaseImpl
from email_service.application.use_case.save_email_use_case_impl import SaveEmailUseCaseImpl
from email_service.application.use_case.send_email_use_case_impl import SendEmailUseCaseImpl
from email_service.domain.exception.email_not_found_exception import EmailNotFoundException
from email_service.domain.model.email import Email
from email_service.domain.serializer.email_serializer import EmailSerializer


class SendEmailView(APIView):
    @inject.params(save_email_use_case=SaveEmailUseCaseImpl, send_email_use_case=SendEmailUseCaseImpl)
    def __init__(self, save_email_use_case: SaveEmailUseCaseImpl, send_email_use_case: SendEmailUseCaseImpl,
                 **kwargs) -> None:
        super().__init__(**kwargs)
        self.save_email_use_case = save_email_use_case
        self.send_email_use_case = send_email_use_case

    def post(self, request: Request) -> Response:
        serializer = EmailSerializer(data=request.data)
        if serializer.is_valid():
            email = Email(**serializer.validated_data)
            email_id = self.save_email_use_case.save(email)
            self.send_email_use_case.send(email)
            location = reverse('email_detail', kwargs={'id': email_id})
            return Response(
                {'message': 'Email sent!'},
                headers={'Location': location},
                status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EmailListView(APIView):
    @inject.params(find_email_use_case=FindEmailUseCaseImpl)
    def __init__(self, find_email_use_case: FindEmailUseCaseImpl, **kwargs) -> None:
        super().__init__(**kwargs)
        self.find_email_use_case = find_email_use_case

    def get(self, request: Request) -> Response[list[Email]]:
        emails = self.find_email_use_case.find_all()
        serializer = EmailSerializer(emails, many=True)
        return Response(serializer.data)


class EmailDetailView(APIView):
    @inject.params(find_email_use_case=FindEmailUseCaseImpl)
    def __init__(self, find_email_use_case: FindEmailUseCaseImpl, **kwargs) -> None:
        super().__init__(**kwargs)
        self.find_email_use_case = find_email_use_case

    def get(self, request: Request, id: int) -> Response[Email]:
        try:
            email = self.find_email_use_case.find_by_id(id)
            serializer = EmailSerializer(email)
            return Response(serializer.data)
        except EmailNotFoundException as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
