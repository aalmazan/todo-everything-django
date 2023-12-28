from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _
from model_utils.models import SoftDeletableModel, TimeStampedModel

ORGANIZATION_ADMIN = "admin"
ORGANIZATION_MEMBER = "member"
ORGANIZATION_GUEST = "guest"
ORGANIZATION_ROLES = [
    (ORGANIZATION_ADMIN, "Admin"),
    (ORGANIZATION_MEMBER, "Member"),
    (ORGANIZATION_GUEST, "Guest"),
]


class Organization(TimeStampedModel, SoftDeletableModel, models.Model):
    """Organization model mainly to group `Account`s."""

    name = models.CharField(max_length=64)
    accounts = models.ManyToManyField(
        get_user_model(),
        through="OrganizationAccounts",
        through_fields=("organization", "account"),
        related_name="organizations",
    )

    class Meta:
        db_table = "organization"
        ordering = ["name"]

    def __str__(self):
        return self.name


class OrganizationAccounts(TimeStampedModel, models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    account = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    # TODO: Add meta things like group, person, inviter (from Django example).
    role = models.CharField(
        max_length=64, choices=ORGANIZATION_ROLES, default=ORGANIZATION_MEMBER
    )

    class Meta:
        db_table = "organization_accounts"
        unique_together = ("organization", "account")


class OrganizationInvite(TimeStampedModel, models.Model):
    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        verbose_name=_("Organization which user was invited to"),
    )
    account_inviter = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        verbose_name=_("Account which created the invitation"),
        related_name="accounts_invited",
    )
    invited_email = models.EmailField(_("Email address of the invitation"))
    # `invited_account` will be populated if the user already had an account
    # or once the user accepts an invitation.
    # Also note that a single user can be invited to many orgs, but should
    # only have one invitation per org.
    invited_account = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        verbose_name=_("Account created from the invitation"),
        null=True,
        default=None,
    )
    role = models.CharField(
        _("Role the invited user will have"),
        max_length=64,
        choices=ORGANIZATION_ROLES,
        default=ORGANIZATION_MEMBER,
    )

    class Meta:
        unique_together = ("organization", "invited_account")
