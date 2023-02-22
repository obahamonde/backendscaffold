"""Object Storage and Data Lake Service."""

from boto3 import Session
from src.config import env


class Cloud(Session):

    """Cloud storage entity for storing frequently used data."""

    def __init__(self):
        super().__init__(
            aws_access_key_id=env.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=env.AWS_SECRET_ACCESS_KEY,
            region_name=env.AWS_REGION,
        )

    @property
    def s3(self):
        """Return the s3 client."""
        return self.client("s3")

    @property
    def func(self):
        """Return the lambda client."""
        return self.client("lambda")

    @property
    def db(self):
        """Return the dynamodb client."""
        return self.client("dynamodb")

    @property
    def ses(self):
        """Return the ses client."""
        return self.client("ses")

    @property
    def comprehend(self):
        """Return the comprehend client."""
        return self.client("comprehend")

    @property
    def rekognition(self):
        """Return the rekognition client."""
        return self.client("rekognition")

    @property
    def translate(self):
        """Return the translate client."""
        return self.client("translate")

    @property
    def polly(self):
        """Return the polly client."""
        return self.client("polly")

    @property
    def lex(self):
        """Return the lex client."""
        return self.client("lex-runtime")

    @property
    def sts(self):
        """Return the sts client."""
        return self.client("sts")

    @property
    def iam(self):
        """Return the iam client."""
        return self.client("iam")