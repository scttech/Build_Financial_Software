FROM dbeaver/cloudbeaver:latest

# Copy automatic server configuration settings
# https://github.com/dbeaver/cloudbeaver/wiki/Server-configuration
COPY ./configuration/cloudbeaver.auto.conf /opt/cloudbeaver/conf/.cloudbeaver.auto.conf

# Copy data sources defined to cloudbeaver
COPY ./configuration/data-sources.json /opt/cloudbeaver/workspace/GlobalConfiguration/.dbeaver/data-sources.json