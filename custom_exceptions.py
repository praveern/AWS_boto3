"""
Custom exceptions defined here.
1. UnidentifiedPolicyError
2. UnidentifiedRoleError
"""


class UnidentifiedPolicyException(Exception):
    """
    Defines an "unknown policy error" and throws out that exception.
    """
    def __init__(self, *args, **kwargs):
        """
        Just calls the Exception class under the hood of the subclass.

        Args:
            args: Optional tuple shaped set of positional args
            kwargs: Optional dictionary shaped keyword args ("key: value" pair stylized)
        """
        super(UnidentifiedPolicyException, self).__init__(*args, **kwargs)


class UnidentifiedRoleException(Exception):
    """
    Defines an "unknown role error" and throws out that exception.
    """
    def __init__(self, *args, **kwargs):
        """
        Just calls the Exception class under the hood of the subclass.

        Args:
            args:
            kwargs:
        """
        super(UnidentifiedRoleException, self).__init__(*args, **kwargs)
