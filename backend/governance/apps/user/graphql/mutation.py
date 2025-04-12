import strawberry

from gqlauth.user import arg_mutations as authmutations


@strawberry.type
class Mutation:
    # include what-ever authmutations you want.
    # verify_token = authmutations.VerifyToken.field
    # update_account = authmutations.UpdateAccount.field
    # archive_account = authmutations.ArchiveAccount.field
    # delete_account = authmutations.DeleteAccount.field
    # password_change = authmutations.PasswordChange.field
    # register = authmutations.Register.field
    # verify_account = authmutations.VerifyAccount.field
    # resend_activation_email = authmutations.ResendActivationEmail.field
    # send_password_reset_email = authmutations.SendPasswordResetEmail.field
    # password_reset = authmutations.PasswordReset.field
    # password_set = authmutations.PasswordSet.field
    # revoke_token = authmutations.RevokeToken.field
    pass


@strawberry.type
class PublicMutation:
    token_auth = authmutations.ObtainJSONWebToken.field
    refresh_token = authmutations.RefreshToken.field