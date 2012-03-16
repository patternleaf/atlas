from datetime import datetime
from lettuce import step, world
from lettuce.django import django_url
from nose.tools import assert_equal
from storybase_user.models import Organization

def save_info(organization_id):
    """ Save an organization's info for later comparison
    
    Assumes that world.browser is in an organization's admin page
    
    """
    world.organization = Organization.objects.get(organization_id=organization_id) 

def assert_organization_unchanged(changed=[]):
    """ Check that the an organization's fields are unchanged 

    Arguments:
    changed -- Array of fields that we know have changed. These will be ignored

    """
    organization = Organization.objects.get(organization_id=world.organization.organization_id)
    for field in ('organization_id', 'website_url', 'description'):
        if field not in changed:
            assert_equal(getattr(world.organization, field),
                getattr(organization, field))

@step(u'Given an admin user creates the Organization "([^"]*)" with website URL "([^"]*)"')
def create(step, name, website_url):
    world.create_admin_user()
    world.admin_login()
    world.browser.click_link_by_href("storybase_user/organization/add/")
    world.browser.fill('name', name)
    world.browser.fill('website_url', website_url)
    world.browser.find_by_name('_save').first.click()
    world.browser.click_link_by_text(name)

@step(u'Then the Organization should have a canonical URL')
def access_url(step):
    organization_id = world.browser.find_by_css('.organization_id p').first.value
    world.assert_is_uuid4(organization_id)
    world.browser.visit(django_url('/organizations/%s' % organization_id))

@step(u'Then the Organization\'s website should be listed as "([^"]*)"')
def see_website_url(step, website_url):
    world.assert_text_present(website_url)

@step(u'Then the Organization\'s members list should be blank')
def no_members(step):
    world.assert_text_not_present('Members')

@step(u'Then the Organization\'s created on field should be set to the current date')
def created_today(step):
    created = datetime.strptime(world.browser.find_by_css('time.created').value,
        '%B %d, %Y')
    world.assert_today(created)

@step(u'Then the Organization\'s last edited field should be set to within 1 minute of the current date and time')
def last_edited_now(step):
    last_edited = datetime.strptime(world.browser.find_by_css('time.last-edited').value,
        '%B %d, %Y %I:%M %p')
    world.assert_now(last_edited, 60)

@step(u'Then the Organization\'s description should be blank')
def blank_description(step):
    world.assert_text_not_present('Description')

@step(u'Given the Organization "([^"]*)" exists')
def exists_in_admin(step, name):
    # Visit the Organization's admin panel
    world.browser.visit(django_url('/admin/storybase_user/organization/'))
    world.browser.click_link_by_text(name)
    organization_id = world.browser.find_by_css('.organization_id p').first.value
    save_info(organization_id)

@step(u'Given the Organization "([^"]*)" has website URL "([^"]*)"')
def has_website_url_in_admin(step, name, website_url):
    # Visit the Organization's admin panel
    world.browser.visit(django_url('/admin/storybase_user/organization/'))
    world.browser.click_link_by_text(name)
    org_website_url = world.browser.find_by_css('#id_website_url').first.value
    assert_equal(org_website_url, website_url)

@step(u'Given the admin user edits the description for the Organization "([^"]*)" to be "([^"]*)"')
def edit_description(step, name, description):
    world.browser.visit(django_url('/admin/storybase_user/organization/'))
    world.browser.click_link_by_text(name)
    world.browser.fill('description', description)
    world.browser.find_by_name('_save').first.click()

@step(u'Then the Organization\'s description is listed as "([^"]*)"')
def see_description(step, description):
    world.browser.visit(django_url('/organizations/%s' % world.organization.organization_id))
    world.assert_text_present(description)

@step(u'Then all other fields of the Organization are unchanged')
def description_changed_others_unchanged(step):
    assert_organization_unchanged(['description'])
