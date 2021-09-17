import logging
import os

from slack_bolt import App
from .models import Order, Gaman

logger = logging.getLogger(__name__)

app = App(
    token=os.environ["SLACK_BOT_TOKEN"],
    signing_secret=os.environ["SLACK_SIGNING_SECRET"],
    # disable eagerly verifying the given SLACK_BOT_TOKEN value
    token_verification_enabled=False,
)


@app.message("uber")
def say_hello(message, say):
    user = message['user']
    say(
        blocks=[
            {
                "type": "section",
                "text": {"type": "mrkdwn", "text": f"<@{user}> もしかしてウーバーした？"},
            },
            {
			"type": "actions",
			"elements": [
				{
					"type": "button",
					"text": {
						"type": "plain_text",
						"text": "したよ",
					},
					"action_id": "button_click",
				},
				{
					"type": "button",
					"text": {
						"type": "plain_text",
						"text": "してないよ",
					},
					"action_id": "button_gaman",
				}
			]
		}
        ],
        text=f"ウーバーアラート発動"
    )


@app.action("button_click")
def open_modal(ack, body, client):
    logger.info(body)
    # Acknowledge the command request
    ack()
    # Call views_open with the built-in client
    client.views_open(
        # Pass a valid trigger_id within 3 seconds of receiving it
        trigger_id=body["trigger_id"],
        # View payload
        view={
            "type": "modal",
            "callback_id": "view_1",
            "title": {
                "type": "plain_text",
                "text": "UberAlert"
            },
            "submit": {
                "type": "plain_text",
                "text": "Submit"
            },
            "blocks": [
                {
                    "block_id": "price",
                    "type": "input",
                    "element": {
                        "type": "plain_text_input",
                        "action_id": "price",
                        "placeholder": {
                            "type": "plain_text",
                                    "text": "1000"
                        }
                    },
                    "label": {
                        "type": "plain_text",
                        "text": "いくらやった？"
                    }
                },
            ],
            "private_metadata": body["container"]["channel_id"]
        }
    )


@app.view("view_1")
def handle_submission(ack, body, client, view, logger):
    logger.info(body)
    # Validate the inputs

    # Acknowledge the view_submission request and close the modal
    ack()
    # Do whatever you want with the input data - here we're saving it to a DB
    # then sending the user a verification of their submission
    user = body["user"]["id"]

    # Message to send user
    msg = ""
    try:
        # Save to DB
        order = Order(user_id=user,price=view["state"]["values"]["price"]["price"]["value"])
        order.save()
    except Exception as e:
        # Handle error
        msg = "There was an error with your submission"

    # Message the user
    count = Order.objects.filter(user_id=user).count()
    sum = 0
    for object in Order.objects.filter(user_id=user).all():
        sum += object.price
    
    msg = f"<@{user}> の注文累計回数{count}回、累計金額{sum}円" 

    
    try:
        client.chat_postMessage(channel=body["view"]["private_metadata"], text=msg)
    except e:
        logger.exception(f"Failed to post a message {e}")

@app.action("button_gaman")
def open_modal(ack, body, client):
    logger.info(body)
    # Acknowledge the command request
    ack()
    # Call views_open with the built-in client
    client.views_open(
        # Pass a valid trigger_id within 3 seconds of receiving it
        trigger_id=body["trigger_id"],
        # View payload
        view={
            "type": "modal",
            "callback_id": "view_gaman",
            "title": {
                "type": "plain_text",
                "text": "UberAlert"
            },
            "submit": {
                "type": "plain_text",
                "text": "Submit"
            },
            "blocks": [
                {
                    "block_id": "price",
                    "type": "input",
                    "element": {
                        "type": "plain_text_input",
                        "action_id": "price",
                        "placeholder": {
                            "type": "plain_text",
                                    "text": "1000"
                        }
                    },
                    "label": {
                        "type": "plain_text",
                        "text": "いくらするつもりやった？"
                    }
                },
            ],
            "private_metadata": body["container"]["channel_id"]
        }
    )


@app.view("view_1")
def handle_submission(ack, body, client, view, logger):
    logger.info(body)
    # Validate the inputs

    # Acknowledge the view_submission request and close the modal
    ack()
    # Do whatever you want with the input data - here we're saving it to a DB
    # then sending the user a verification of their submission
    user = body["user"]["id"]

    # Message to send user
    msg = ""
    try:
        # Save to DB
        order = Order(user_id=user,price=view["state"]["values"]["price"]["price"]["value"])
        order.save()
    except Exception as e:
        # Handle error
        msg = "There was an error with your submission"

    # Message the user
    count = Order.objects.filter(user_id=user).count()
    sum = 0
    for object in Order.objects.filter(user_id=user).all():
        sum += object.price
    
    msg = f"<@{user}> の注文累計回数{count}回、累計金額{sum}円" 

    
    try:
        client.chat_postMessage(channel=body["view"]["private_metadata"], text=msg)
    except e:
        logger.exception(f"Failed to post a message {e}")

@app.view("view_gaman")
def handle_submission(ack, body, client, view, logger):
    logger.info(body)
    # Validate the inputs

    # Acknowledge the view_submission request and close the modal
    ack()
    # Do whatever you want with the input data - here we're saving it to a DB
    # then sending the user a verification of their submission
    user = body["user"]["id"]

    # Message to send user
    msg = ""
    try:
        # Save to DB
        gaman = Gaman(user_id=user,price=view["state"]["values"]["price"]["price"]["value"])
        gaman.save()
    except Exception as e:
        # Handle error
        msg = "There was an error with your submission"

    # Message the user
    count = Gaman.objects.filter(user_id=user).count()
    sum = 0
    for object in Gaman.objects.filter(user_id=user).all():
        sum += object.price
    
    msg = f"<@{user}> の累計我慢回数{count}回、累計我慢金額{sum}円" 

    
    try:
        client.chat_postMessage(channel=body["view"]["private_metadata"], text=msg)
    except e:
        logger.exception(f"Failed to post a message {e}")

@app.command("/uber")
def command_uber(ack, say, client, respond, command, body):
    # Acknowledge command request
    ack()
    user = body["user_id"]
    args = command["text"].split()

    if args[0] == "history":
        if not Order.objects.filter(user_id=user).exists():
            say("注文履歴はありません")
            return

        response = client.chat_postMessage(
            channel=body["channel_id"],
            text=f"<@{user}>さんの注文履歴:tsuduki_ha_thread_de:"
        )
        for object in Order.objects.filter(user_id=user):
            client.chat_postMessage(
                channel=body["channel_id"],
                thread_ts=response["ts"],
                text=f"ID: {object.id}, Price: {object.price}, Date: {object.ordered_at}"
            )

    if args[0] == "delete":
        if not Order.objects.filter(id=args[1], user_id=user).exists():
            respond(f"不正なIDです。({args[1]})")
            return

        object = Order.objects.get(id=args[1], user_id=user)
        respond(f"指定された注文履歴を削除するね。\nID: {object.id}, Price: {object.price}, Date: {object.ordered_at}")
        object.delete()