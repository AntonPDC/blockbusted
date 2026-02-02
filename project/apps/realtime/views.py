"""HTTP endpoint that triggers a websocket broadcast.

We keep this as a standard DRF view because it's often convenient:
- admin clicks a button in a dashboard
- a cron job triggers a refresh
- a CI deployment triggers the clients to refetch

Permission is admin-only by default.
"""

from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

class RefetchBroadcastView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def post(self, request):
        channel_layer = get_channel_layer()

        # Broadcast to all sockets in the "movies" group
        async_to_sync(channel_layer.group_send)(
            "movies",
            {"type": "refetch_movies", "message": "refetch movies"},
        )

        return Response({"sent": True})
