"""Centralized RBAC — roles and permissions."""

from __future__ import annotations

from enum import Enum
from typing import Dict, FrozenSet, Set


class Role(str, Enum):
    ANALYST = "analyst"
    MANAGER = "manager"
    ADMIN = "admin"
    AUDITOR = "auditor"


class Permission(str, Enum):
    ENTITIES_READ = "entities.read"
    ALERTS_READ = "alerts.read"
    ALERTS_ACTION = "alerts.action"
    CASES_READ = "cases.read"
    CASES_WRITE = "cases.write"
    CASES_ASSIGN = "cases.assign"
    USERS_MANAGE = "users.manage"
    AUDIT_READ = "audit.read"
    AUDIT_WRITE = "audit.write"  # never granted to application users
    REPORTS_READ = "reports.read"
    REPORTS_GENERATE = "reports.generate"


ROLE_PERMISSIONS: Dict[Role, FrozenSet[Permission]] = {
    Role.ANALYST: frozenset({
        Permission.ENTITIES_READ, Permission.ALERTS_READ, Permission.ALERTS_ACTION,
        Permission.CASES_READ, Permission.CASES_WRITE, Permission.REPORTS_READ, Permission.REPORTS_GENERATE,
    }),
    Role.MANAGER: frozenset({
        Permission.ENTITIES_READ, Permission.ALERTS_READ, Permission.ALERTS_ACTION,
        Permission.CASES_READ, Permission.CASES_WRITE, Permission.CASES_ASSIGN,
        Permission.REPORTS_READ, Permission.REPORTS_GENERATE, Permission.AUDIT_READ,
    }),
    Role.ADMIN: frozenset({
        Permission.ENTITIES_READ, Permission.ALERTS_READ, Permission.ALERTS_ACTION,
        Permission.CASES_READ, Permission.CASES_WRITE, Permission.CASES_ASSIGN,
        Permission.USERS_MANAGE, Permission.AUDIT_READ, Permission.REPORTS_READ, Permission.REPORTS_GENERATE,
    }),
    Role.AUDITOR: frozenset({
        Permission.ENTITIES_READ, Permission.ALERTS_READ, Permission.CASES_READ,
        Permission.AUDIT_READ, Permission.REPORTS_READ,
    }),
}

ALERT_ACTION_PERMISSIONS: Dict[str, FrozenSet[Role]] = {
    "flag": frozenset({Role.ANALYST, Role.MANAGER, Role.ADMIN}),
    "escalate": frozenset({Role.ANALYST, Role.MANAGER, Role.ADMIN}),
    "dismiss": frozenset({Role.MANAGER, Role.ADMIN}),
    "freeze": frozenset({Role.MANAGER, Role.ADMIN}),
    "report": frozenset({Role.MANAGER, Role.ADMIN}),
}


def permissions_for_role(role: Role | str) -> Set[Permission]:
    r = Role(role) if isinstance(role, str) else role
    return set(ROLE_PERMISSIONS.get(r, frozenset()))


def has_permission(role: Role | str, permission: Permission | str) -> bool:
    perm = Permission(permission) if isinstance(permission, str) else permission
    return perm in permissions_for_role(role)


def can_perform_alert_action(role: Role | str, action: str) -> bool:
    r = Role(role) if isinstance(role, str) else role
    allowed = ALERT_ACTION_PERMISSIONS.get(action)
    if allowed is None:
        return False
    return r in allowed
