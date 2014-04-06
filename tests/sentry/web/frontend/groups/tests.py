# -*- coding: utf-8 -*-

from __future__ import absolute_import

import json

from datetime import timedelta
from django.core.urlresolvers import reverse
from django.utils import timezone
from exam import fixture

from sentry.constants import MAX_JSON_RESULTS
from sentry.testutils import TestCase


class GroupEventListTest(TestCase):
    @fixture
    def path(self):
        return reverse('sentry-group-events', kwargs={
            'team_slug': self.team.slug,
            'project_id': self.project.slug,
            'group_id': self.group.id,
        })

    def test_does_render(self):
        event = self.create_event(
            event_id='a' * 32, datetime=timezone.now() - timedelta(minutes=1))
        event2 = self.create_event(
            event_id='b' * 32, datetime=timezone.now())

        self.login()
        resp = self.client.get(self.path)
        assert resp.status_code == 200
        self.assertTemplateUsed(resp, 'sentry/groups/event_list.html')
        assert 'group' in resp.context
        assert 'project' in resp.context
        assert 'team' in resp.context
        assert 'event_list' in resp.context
        assert resp.context['project'] == self.project
        assert resp.context['team'] == self.team
        assert resp.context['group'] == self.group
        event_list = resp.context['event_list']
        assert len(event_list) == 2
        assert event_list[0] == event2
        assert event_list[1] == event


class GroupTagListTest(TestCase):
    @fixture
    def path(self):
        return reverse('sentry-group-tags', kwargs={
            'team_slug': self.team.slug,
            'project_id': self.project.slug,
            'group_id': self.group.id,
        })

    def test_does_render(self):
        self.login()
        resp = self.client.get(self.path)
        assert resp.status_code == 200
        self.assertTemplateUsed(resp, 'sentry/groups/tag_list.html')
        assert 'group' in resp.context
        assert 'project' in resp.context
        assert 'team' in resp.context
        assert 'tag_list' in resp.context
        assert resp.context['project'] == self.project
        assert resp.context['team'] == self.team
        assert resp.context['group'] == self.group


class GroupEventDetailsTest(TestCase):
    @fixture
    def path(self):
        return reverse('sentry-group-event', kwargs={
            'team_slug': self.team.slug,
            'project_id': self.project.slug,
            'group_id': self.group.id,
            'event_id': self.event.id,
        })

    def test_does_render(self):
        self.login()
        resp = self.client.get(self.path)
        assert resp.status_code == 200
        self.assertTemplateUsed(resp, 'sentry/groups/details.html')
        assert 'group' in resp.context
        assert 'project' in resp.context
        assert 'team' in resp.context
        assert 'event' in resp.context
        assert resp.context['project'] == self.project
        assert resp.context['team'] == self.team
        assert resp.context['group'] == self.group
        assert resp.context['event'] == self.event


class GroupEventListJsonTest(TestCase):
    @fixture
    def path(self):
        return reverse('sentry-group-events-json', kwargs={
            'team_slug': self.team.slug,
            'project_id': self.project.slug,
            'group_id': self.group.id,
        })

    def test_does_render(self):
        self.login()

        event = self.create_event(
            event_id='a' * 32, datetime=timezone.now() - timedelta(minutes=1))
        event2 = self.create_event(
            event_id='b' * 32, datetime=timezone.now())

        resp = self.client.get(self.path)
        assert resp.status_code == 200
        assert resp['Content-Type'] == 'application/json'
        data = json.loads(resp.content)
        assert len(data) == 2
        assert data[0]['id'] == str(event2.event_id)
        assert data[1]['id'] == str(event.event_id)

    def test_does_not_allow_beyond_limit(self):
        self.login()
        resp = self.client.get(self.path, {'limit': MAX_JSON_RESULTS + 1})
        assert resp.status_code == 400


class GroupEventJsonTest(TestCase):
    @fixture
    def path(self):
        return reverse('sentry-group-event-json', kwargs={
            'team_slug': self.team.slug,
            'project_id': self.project.slug,
            'group_id': self.group.id,
            'event_id_or_latest': self.event.id,
        })

    def test_does_render(self):
        self.login()
        resp = self.client.get(self.path)
        assert resp.status_code == 200
        assert resp['Content-Type'] == 'application/json'
        data = json.loads(resp.content)
        assert data['id'] == self.event.event_id
