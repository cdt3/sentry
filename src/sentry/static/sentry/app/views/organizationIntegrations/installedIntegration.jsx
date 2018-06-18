import {Box} from 'grid-emotion';
import PropTypes from 'prop-types';
import React from 'react';

import {PanelItem} from 'app/components/panels';
import {t} from 'app/locale';
import Button from 'app/components/buttons/button';
import Confirm from 'app/components/confirm';
import IntegrationItem from 'app/views/organizationIntegrations/integrationItem';

const CONFIGURABLE_FEATURES = ['commits'];

export default class InstalledIntegration extends React.Component {
  static propTypes = {
    orgId: PropTypes.string.isRequired,
    provider: PropTypes.object.isRequired,
    integration: PropTypes.object.isRequired,
    onRemove: PropTypes.func.isRequired,
  };

  /**
   * Integrations have additional configuration when any of the conditions are
   * met:
   *
   * - The Integration has organization-specific configuration options.
   * - The Integration can be enabled for projects.
   * - The Integration has configurable features
   */
  hasConfiguration() {
    const {integration, provider} = this.props;

    return (
      integration.configProject.length > 0 ||
      provider.canAddProject ||
      provider.features.filter(f => CONFIGURABLE_FEATURES.includes(f)).length > 0
    );
  }

  render() {
    const {integration, provider, orgId} = this.props;

    return (
      <React.Fragment>
        <PanelItem p={0} py={2} key={integration.id} align="center">
          <Box px={2} flex={1}>
            <IntegrationItem integration={integration} />
          </Box>
          {this.hasConfiguration() && (
            <Box mr={1}>
              <Button
                size="small"
                to={`/settings/${orgId}/integrations/${provider.key}/${integration.id}/`}
              >
                {t('Configure')}
              </Button>
            </Box>
          )}
          <Box mr={1} pr={2}>
            <Confirm
              message={t(
                'Removing this inegration will disable the integration for all projects. Are you sure you want to remove this integration?'
              )}
              onConfirm={() => this.props.onRemove()}
            >
              <Button size="small" icon="icon-trash" />
            </Confirm>
          </Box>
        </PanelItem>
      </React.Fragment>
    );
  }
}
