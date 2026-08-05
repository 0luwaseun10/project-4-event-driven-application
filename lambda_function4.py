import json
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    logger.info("Received event: %s", json.dumps(event))

    processed_orders = []

    for record in event.get("Records", []):
        # SQS contains an SNS notification envelope.
        sns_notification = json.loads(record["body"])
        order = json.loads(sns_notification["Message"])

        order_id = order.get("orderId")

        if not order_id:
            raise ValueError("The order is missing an orderId.")

        # Used later to test retries and the dead-letter queue.
        if order.get("status") == "FAIL":
            raise RuntimeError(f"Simulated failure for order {order_id}")

        logger.info(
            "Processed order %s for %s: %s x%s",
            order_id,
            order.get("customerName"),
            order.get("item"),
            order.get("quantity"),
        )

        processed_orders.append(order_id)

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "Orders processed successfully",
            "processedOrders": processed_orders,
        }),
    }