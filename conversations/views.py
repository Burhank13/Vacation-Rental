from django.db.models import Q
from django.http import Http404
from django.shortcuts import redirect, reverse, render
from django.views.generic import View
from users import models as user_models
from . import models


def go_conversation(request, a_pk, b_pk):

    try:
        user_one = user_models.User.objects.get(pk=a_pk)
    except user_one.DoesNotExist:
        user_one = None

    try:
        user_two = user_models.User.objects.get(pk=b_pk)
    except user_two.DoesNotExist:
        user_two = None

    print(user_one, user_two)

    # user_one = user_models.User.objects.get_or_none(pk=a_pk)
    # user_two = user_models.User.objects.get_or_none(pk=b_pk)
    try:
        conversation = models.Conversation.objects.get(Q(participants=user_one) and
            Q(participants=user_two))
        print(conversation)
    except models.Conversation.DoesNotExist:
        conversation = models.Conversation.objects.create()
        conversation.participants.add(user_one, user_two)
    return redirect(reverse("conversations:detail", kwargs={"pk": conversation.pk}))


class ConversationDetailView(View):
    def get(self, *args, **kwargs):
        pk = kwargs.get("pk")
        conversation = models.Conversation.objects.get(pk=pk)
        print("get",type(conversation))
        if not conversation:
            raise Http404()
        return render(
            self.request,
            "conversations/conversation_detail.html",
            {"conversation": conversation},
        )

    def post(self, *args, **kwargs):
        message = self.request.POST.get("message", None)
        pk = kwargs.get("pk")
        conversation = models.Conversation.objects.get_or_none(pk=pk)
        print("post", conversation)
        if not conversation:
            raise Http404()
        if message is not None:
            models.Message.objects.create(
                message=message, user=self.request.user, conversation=conversation
            )
        return redirect(reverse("conversations:detail", kwargs={"pk": pk}))


class conver_list(View):
    def get(self, *args, **kwargs):
        current_user = self.request.user
        # pk = kwargs.get("pk")
        conversation = models.Conversation.objects.filter(participants=current_user)
        return render(self.request, "conversations/conversation_list.html", {
             "conversation": conversation})
