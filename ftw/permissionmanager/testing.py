from plone.app.testing import PloneSandboxLayer
from plone.app.testing import applyProfile
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import IntegrationTesting
from plone.testing import z2
from zope.configuration import xmlconfig
from plone.app.testing import setRoles, TEST_USER_ID, TEST_USER_NAME, login
import ftw.permissionmanager


TEST_USER_ID_2 = '_test_user_2_'
TEST_USER_PW_2 = 'secret'
TEST_GROUP_ID = 'test_group'
TEST_GROUP_ID_2 = 'test_group_2'


class FtwPermissionmanagerLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE, )

    def setUpZope(self, app, configurationContext):
        # Load ZCML

        xmlconfig.file('configure.zcml',
            ftw.permissionmanager,
            context=configurationContext)

        # installProduct() is *only* necessary for packages outside
        # the Products.* namespace which are also declared as Zope 2 products,
        # using <five:registerPackage /> in ZCML.
        z2.installProduct(app, 'ftw.permissionmanager')

    def setUpPloneSite(self, portal):
        # Install into Plone site using portal_setup
        applyProfile(portal, 'ftw.permissionmanager:default')

        setRoles(portal, TEST_USER_ID, ['Manager'])
        login(portal, TEST_USER_NAME)
        # Create one folder with one item
        portal.invokeFactory('Folder', 'folder1', title='Folder1')
        portal.folder1.invokeFactory('Folder', 'folder2', title='Folder2')

        # Add a new user
        portal.portal_registration.addMember(TEST_USER_ID_2, TEST_USER_PW_2)


FTW_PERMISSIONMANAGER_FIXTURE = FtwPermissionmanagerLayer()
FTW_PERMISSIONMANAGER_INTEGRATION_TESTING = IntegrationTesting(
    bases=(FTW_PERMISSIONMANAGER_FIXTURE, ),
    name="ftw.permissionmanager:Integration")
