# Working with Azure AI projects on your compute instance

## The Azure AI Folder Hierarchy

The Azure AI folder hierarchy (`afh`) is designed to orient you within your current working context, and help you work with your code, data and shared files most efficiently. This `afh` directory houses your Azure AI projects, and each specific project's folder has a `code`, `data` and `shared` folder.

Files, folders, and repos you store in your project folder persist across compute instance restarts but are lost if the machine is deleted.

### The `code` and `data` folders

- Use `code` for working with git repositories and private code files
- Use `data` for storing private data files

The `code` folder is where we recommend you clone your git repositories, or otherwise bring in or create your code files. This is a storage location directly on your compute instance, and will be performant for large repositories. We recommend you use the `data` folder to store and reference local or private data in a consistent way.

### The `shared` folder

- Use `shared` for working with a project's shared files and assets
- Use `shared\Users\{user-name}\promptflow` to reference and edit prompt flows

The `shared` folder is where you will find the project's shared files and assets, including prompt flows that are developed in the Azure AI Studio. To find specific files or flows, navigate to the relevant user folder. Flows will be in the `promptflow` folder.

## Get started with the AI Studio custom container for VS Code

For those that launched VS Code from the Azure AI Studio, you are remotely connected to a custom container running on your compute instance. The file explorer is loaded in a dedicated folder for the project you were working on in the Azure AI Studio. This development environment comes pre-configured with the Azure AI SDK packages, including Prompt flow, and the [Azure Developer CLI (azd)](https://learn.microsoft.com/azure/developer/azure-developer-cli/overview).

To get started in your local development environment instead, follow this [quickstart tutorial](https://learn.microsoft.com/azure/ai-studio/quickstarts/get-started-code).

You can also learn more about the [Azure AI SDKs](<https://aka.ms/aistudio/docs/sdk>).


### Working with the Azure AI SDKs

To get started building solutions with the AI SDKs, we recommend the [AI Studio RAG copilot sample](https://github.com/Azure-Samples/rag-data-openai-python-promptflow) as a comprehensive starter repository that shows you how to develop, evaluate and deploy a rag-based copilot.

For a curated list of samples, check out [AI App Templates](aka.ms/azd-ai-templates).

#### Get started with samples in this cloud development environment

1. Open a terminal
1. Clone the sample repository you want into your project's `code` folder. You may be prompted to authenticate to Github

```bash
cd code
git clone https://github.com/Azure-Samples/rag-data-openai-python-promptflow.git
```

3. Navigate to and follow the README

### Working with prompt flows

You can use the Prompt flow SDK and CLI to create and work with prompt flows.

Prompt flows already created in the Azure AI Studio can be found at `shared\Users\{user-name}\promptflow`. You can also create new flows in your `code` or `shared` folder.

The samples show you how Prompt flow is integrated into the application code. You can work with the Prompt flow SDK alongside the Azure SDK to develop, evaluate, and deploy your applications.

You can also use the Prompt flow CLI or Prompt flow VS Code extension (pre-installed in this environment) for capabilities you prefer to work with outside of code. See [prompt flow capabilities](<https://microsoft.github.io/promptflow/reference/index.html>) for more details.

### Client application development

For client app developers seeking cross-language compatibility and seamless integration of OpenAI capabilities, resource provisioning, and deployment, explore the Azure AI Hub at <https://aka.ms/azai>. Discover app templates and SDK samples in your preferred programming language. The app templates are integrated with the [Azure Developer CLI (azd)](https://learn.microsoft.com/azure/developer/azure-developer-cli/overview) that provides you infrastructure-as-code to streamline deploying your applications.
