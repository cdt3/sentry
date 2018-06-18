import React from 'react';

import {t} from 'app/locale';
import AsyncView from 'app/views/asyncView';
import Form from 'app/views/settings/components/forms/form';
import IntegrationItem from 'app/views/organizationIntegrations/integrationItem';
import IntegrationProjects from 'app/views/organizationIntegrations/integrationProjects';
import IntegrationRepos from 'app/views/organizationIntegrations/integrationRepos';
import JsonForm from 'app/views/settings/components/forms/jsonForm';
import SettingsPageHeader from 'app/views/settings/components/settingsPageHeader';

export default class ConfigureIntegration extends AsyncView {
  getEndpoints() {
    const {orgId, integrationId} = this.props.params;

    return [
      ['config', `/organizations/${orgId}/config/integrations/`],
      ['integration', `/organizations/${orgId}/integrations/${integrationId}/`],
    ];
  }

  renderBody() {
    const {orgId} = this.props.params;
    const {integration} = this.state;
    const provider = this.state.config.providers.find(
      p => p.key === integration.provider.key
    );

    const title = <IntegrationItem integration={integration} withProvider={true} />;

    return (
      <React.Fragment>
        <SettingsPageHeader noStyles title={title} />

        {integration.configOrganization.length > 0 && (
          <Form
            hideFooter={true}
            saveOnBlur={true}
            allowUndo={true}
            apiMethod="POST"
            initialData={integration.configData}
            apiEndpoint={`/organizations/${orgId}/integrations/${integration.id}/`}
          >
            <JsonForm fields={integration.configOrganization} title={t('Settings')} />
          </Form>
        )}

        {provider.canAddProject && <IntegrationProjects integrationId={integration.id} />}

        {provider.features.includes('commits') && (
          <IntegrationRepos integration={integration} />
        )}
      </React.Fragment>
    );
  }
}
