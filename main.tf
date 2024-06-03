provider "azurerm" {
  features {}
}

resource "azurerm_resource_group" "ml_rg" {
  name     = "my2ndMLResourceGroup"
  location = "West Europe"
}

resource "azurerm_application_insights" "app_insights" {
  name                = "my2ndAppInsights"
  location            = azurerm_resource_group.ml_rg.location
  resource_group_name = azurerm_resource_group.ml_rg.name
  application_type    = "web"
}

resource "azurerm_key_vault" "kv" {
  name                = "uniqueKeyVaultName2nd" # Ensure this name is globally unique
  location            = azurerm_resource_group.ml_rg.location
  resource_group_name = azurerm_resource_group.ml_rg.name
  tenant_id           = "ad78d191-1044-4303-8212-b6f4dd7874bc"

  sku_name = "standard"
}

resource "azurerm_storage_account" "storage_account" {
  name                     = "2nduniquestorageacct" # Ensure this name is globally unique
  resource_group_name      = azurerm_resource_group.ml_rg.name
  location                 = azurerm_resource_group.ml_rg.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}

resource "azurerm_machine_learning_workspace" "ml_workspace" {
  name                = "my2ndNewMLWorkspace"
  location            = azurerm_resource_group.ml_rg.location
  resource_group_name = azurerm_resource_group.ml_rg.name

  application_insights_id = azurerm_application_insights.app_insights.id
  key_vault_id            = azurerm_key_vault.kv.id
  storage_account_id      = azurerm_storage_account.storage_account.id

  identity {
    type = "SystemAssigned"
  }
}

resource "azurerm_machine_learning_compute_cluster" "cpu_cluster" {
  name                          = "cpu-cluster2nd"
  location                      = azurerm_resource_group.ml_rg.location
  machine_learning_workspace_id = azurerm_machine_learning_workspace.ml_workspace.id
  vm_size                       = "STANDARD_DS11_V2"
  vm_priority                   = "Dedicated"

  scale_settings {
    min_node_count                       = 0
    max_node_count                       = 4
    scale_down_nodes_after_idle_duration = "PT5M"
  }
}