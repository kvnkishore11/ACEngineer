AgenticKanban Architecture Plan: Project-Centric ADW Orchestration                                                 │ │
│ │                                                                                                                    │ │
│ │ Vision                                                                                                             │ │
│ │                                                                                                                    │ │
│ │ Transform AgenticKanban into an Electron app that serves as a universal visual interface for AI development        │ │
│ │ workflows, where each client project contains its own intelligent orchestration logic.                             │ │
│ │                                                                                                                    │ │
│ │ Core Philosophy: "VS Code for AI Workflows"                                                                        │ │
│ │                                                                                                                    │ │
│ │ - Kanban Board: Universal interface (like VS Code editor)                                                          │ │
│ │ - Client Projects: Contains domain-specific intelligence (like language extensions)                                │ │
│ │ - ADW Scripts: Project-specific workflow implementations (like project configurations)                             │ │
│ │                                                                                                                    │ │
│ │ ---                                                                                                                │ │
│ │ Architecture Overview                                                                                              │ │
│ │                                                                                                                    │ │
│ │ ┌─────────────────────────────────────────────────────────────┐                                                    │ │
│ │ │  KANBAN BOARD (Electron App) - Universal Interface         │                                                     │ │
│ │ │  ┌─────────┬─────────┬─────────┬─────────┬─────────┬──────┐ │                                                    │ │
│ │ │  │ Backlog │  Plan   │  Build  │  Test   │ Review  │  PR  │ │                                                    │ │
│ │ │  │         │         │         │         │         │      │ │                                                    │ │
│ │ │  └─────────┴─────────┴─────────┴─────────┴─────────┴──────┘ │                                                    │ │
│ │ │                                                              │                                                   │ │
│ │ │  Actions: Send Task Data → Watch State → Display Progress   │                                                    │ │
│ │ └─────────────────────────────────────────────────────────────┘                                                    │ │
│ │                             │                                                                                      │ │
│ │                     Single Entry Point                                                                             │ │
│ │                             ▼                                                                                      │ │
│ │ ┌─────────────────────────────────────────────────────────────┐                                                    │ │
│ │ │  CLIENT PROJECT - Contains Domain Intelligence             │                                                     │ │
│ │ │  my-ecommerce-app/                                          │                                                    │ │
│ │ │    ├── agentics/adws/                                       │                                                    │ │
│ │ │    │   ├── adw_orchestrator.py    ← PROJECT BRAIN          │                                                     │ │
│ │ │    │   ├── adw_plan.py           ← E-commerce planning     │                                                     │ │
│ │ │    │   ├── adw_build.py          ← E-commerce building     │                                                     │ │
│ │ │    │   ├── adw_security_scan.py  ← Domain-specific stage   │                                                     │ │
│ │ │    │   └── config.json           ← Project preferences     │                                                     │ │
│ │ │    ├── agents/{adw_id}/                                     │                                                    │ │
│ │ │    │   └── adw_state.json        ← State Management        │                                                     │ │
│ │ │    └── .claude/commands/         ← AI Primitives           │                                                     │ │
│ │ └─────────────────────────────────────────────────────────────┘                                                    │ │
│ │                                                                                                                    │ │
│ │ ---                                                                                                                │ │
│ │ Phase 1: Remove Centralized Orchestration                                                                          │ │
│ │                                                                                                                    │ │
│ │ Current Problem                                                                                                    │ │
│ │                                                                                                                    │ │
│ │ ❌ Kanban decides workflow order                                                                                    │ │
│ │ ❌ Kanban spawns individual stage scripts                                                                           │ │
│ │ ❌ Orchestration logic in Kanban system                                                                             │ │
│ │ ❌ One-size-fits-all approach                                                                                       │ │
│ │                                                                                                                    │ │
│ │ Solution                                                                                                           │ │
│ │                                                                                                                    │ │
│ │ ✅ Kanban sends task data to project                                                                                │ │
│ │ ✅ Project decides workflow order                                                                                   │ │
│ │ ✅ Project orchestrates its own execution                                                                           │ │
│ │ ✅ Domain-specific intelligence per project                                                                         │ │
│ │                                                                                                                    │ │
│ │ Cleanup Tasks                                                                                                      │ │
│ │                                                                                                                    │ │
│ │ 1. Remove from AgenticKanban:                                                                                      │ │
│ │   - WebSocket service and API calls                                                                                │ │
│ │   - Stage orchestration logic in kanbanStore.js                                                                    │ │
│ │   - Individual stage spawning logic                                                                                │ │
│ │   - Pipeline management in frontend                                                                                │ │
│ │ 2. Remove from tac-7 copy:                                                                                         │ │
│ │   - kanban_api.py FastAPI server                                                                                   │ │
│ │   - WebSocket simulation logic                                                                                     │ │
│ │   - workflow_executor.py complexity                                                                                │ │
│ │                                                                                                                    │ │
│ │ ---                                                                                                                │ │
│ │ Phase 2: Electron Conversion                                                                                       │ │
│ │                                                                                                                    │ │
│ │ Setup Universal Interface                                                                                          │ │
│ │                                                                                                                    │ │
│ │ // Electron main process - Universal project handler                                                               │ │
│ │ class UniversalADWInterface {                                                                                      │ │
│ │   async executeWorkflow(projectPath, taskData) {                                                                   │ │
│ │     // Single entry point for ANY project                                                                          │ │
│ │     const orchestratorPath = `${projectPath}/agentics/adws/adw_orchestrator.py`;                                   │ │
│ │                                                                                                                    │ │
│ │     return spawn('python', [orchestratorPath, JSON.stringify(taskData)], {                                         │ │
│ │       cwd: `${projectPath}/agentics/adws`,                                                                         │ │
│ │       stdio: ['pipe', 'pipe', 'pipe']                                                                              │ │
│ │     });                                                                                                            │ │
│ │   }                                                                                                                │ │
│ │                                                                                                                    │ │
│ │   watchProjectState(projectPath, adwId, callback) {                                                                │ │
│ │     // Watch any project's state files                                                                             │ │
│ │     const statePath = `${projectPath}/agentics/agents/${adwId}/adw_state.json`;                                    │ │
│ │     chokidar.watch(statePath).on('change', () => {                                                                 │ │
│ │       const state = JSON.parse(fs.readFileSync(statePath, 'utf8'));                                                │ │
│ │       callback(state);                                                                                             │ │
│ │     });                                                                                                            │ │
│ │   }                                                                                                                │ │
│ │ }                                                                                                                  │ │
│ │                                                                                                                    │ │
│ │ Simplified Kanban Store                                                                                            │ │
│ │                                                                                                                    │ │
│ │ export const useKanbanStore = create((set, get) => ({                                                              │ │
│ │   // Project management                                                                                            │ │
│ │   currentProject: null,                                                                                            │ │
│ │   tasks: [],                                                                                                       │ │
│ │                                                                                                                    │ │
│ │   // Universal actions                                                                                             │ │
│ │   selectProject: (projectPath) => {                                                                                │ │
│ │     set({ currentProject: projectPath });                                                                          │ │
│ │     get().discoverExistingWorkflows(projectPath);                                                                  │ │
│ │   },                                                                                                               │ │
│ │                                                                                                                    │ │
│ │   createTask: async (taskData) => {                                                                                │ │
│ │     const adwId = generateAdwId();                                                                                 │ │
│ │                                                                                                                    │ │
│ │     // Send to project's orchestrator - that's it!                                                                 │ │
│ │     await window.electronAPI.executeWorkflow(                                                                      │ │
│ │       get().currentProject,                                                                                        │ │
│ │       { ...taskData, adw_id: adwId }                                                                               │ │
│ │     );                                                                                                             │ │
│ │                                                                                                                    │ │
│ │     // Start watching for state changes                                                                            │ │
│ │     get().watchTaskState(adwId);                                                                                   │ │
│ │   },                                                                                                               │ │
│ │                                                                                                                    │ │
│ │   // No orchestration logic here - just UI management                                                              │ │
│ │   updateTaskFromState: (adwId, stateData) => {                                                                     │ │
│ │     // Convert ADWState to UI format                                                                               │ │
│ │     const uiTask = convertStateToTask(stateData);                                                                  │ │
│ │     set(state => ({                                                                                                │ │
│ │       tasks: state.tasks.map(task =>                                                                               │ │
│ │         task.metadata?.adwId === adwId ? uiTask : task                                                             │ │
│ │       )                                                                                                            │ │
│ │     }));                                                                                                           │ │
│ │   }                                                                                                                │ │
│ │ }));                                                                                                               │ │
│ │                                                                                                                    │ │
│ │ ---                                                                                                                │ │
│ │ Phase 3: Project-Centric Orchestration                                                                             │ │
│ │                                                                                                                    │ │
│ │ ADW Orchestrator (Project Brain)                                                                                   │ │
│ │                                                                                                                    │ │
│ │ # /client-project/agentics/adws/adw_orchestrator.py                                                                │ │
│ │ class ProjectADWOrchestrator:                                                                                      │ │
│ │     def __init__(self, project_root):                                                                              │ │
│ │         self.project_root = project_root                                                                           │ │
│ │         self.config = self.load_project_config()                                                                   │ │
│ │                                                                                                                    │ │
│ │     def execute_workflow(self, task_data):                                                                         │ │
│ │         """Each project defines its own workflow logic"""                                                          │ │
│ │         adw_id = task_data["adw_id"]                                                                               │ │
│ │                                                                                                                    │ │
│ │         # Create initial state                                                                                     │ │
│ │         state = ADWState(                                                                                          │ │
│ │             adw_id=adw_id,                                                                                         │ │
│ │             issue_title=task_data["title"],                                                                        │ │
│ │             issue_description=task_data["description"],                                                            │ │
│ │             issue_class=task_data["work_item_type"]                                                                │ │
│ │         )                                                                                                          │ │
│ │                                                                                                                    │ │
│ │         # PROJECT-SPECIFIC PIPELINE LOGIC                                                                          │ │
│ │         state.pipeline = self.determine_pipeline(task_data)                                                        │ │
│ │         state.save()                                                                                               │ │
│ │                                                                                                                    │ │
│ │         # Execute pipeline                                                                                         │ │
│ │         self.execute_pipeline(state)                                                                               │ │
│ │                                                                                                                    │ │
│ │     def determine_pipeline(self, task_data):                                                                       │ │
│ │         """Each project has its own pipeline logic"""                                                              │ │
│ │         work_type = task_data["work_item_type"]                                                                    │ │
│ │         description = task_data["description"].lower()                                                             │ │
│ │                                                                                                                    │ │
│ │         # E-commerce project example:                                                                              │ │
│ │         if work_type == "feature":                                                                                 │ │
│ │             if "auth" in description:                                                                              │ │
│ │                 return ["plan", "build", "security_scan", "test", "review"]                                        │ │
│ │             elif "payment" in description:                                                                         │ │
│ │                 return ["plan", "build", "compliance_check", "test", "review"]                                     │ │
│ │             else:                                                                                                  │ │
│ │                 return ["plan", "build", "test", "review"]                                                         │ │
│ │         elif work_type == "bug":                                                                                   │ │
│ │             return ["debug", "fix", "test"]                                                                        │ │
│ │                                                                                                                    │ │
│ │         # Fallback to user selection                                                                               │ │
│ │         return task_data.get("selected_stages", ["plan", "build"])                                                 │ │
│ │                                                                                                                    │ │
│ │ Domain-Specific Stage Implementations                                                                              │ │
│ │                                                                                                                    │ │
│ │ # E-commerce project's planning stage                                                                              │ │
│ │ # /ecommerce-project/agentics/adws/adw_plan.py                                                                     │ │
│ │ def main():                                                                                                        │ │
│ │     adw_id = sys.argv[1]                                                                                           │ │
│ │     state = ADWState.load(adw_id)                                                                                  │ │
│ │                                                                                                                    │ │
│ │     # E-commerce specific planning logic                                                                           │ │
│ │     if "payment" in state.issue_description.lower():                                                               │ │
│ │         template = "ecommerce_payment_planning.md"                                                                 │ │
│ │     elif "inventory" in state.issue_description.lower():                                                           │ │
│ │         template = "ecommerce_inventory_planning.md"                                                               │ │
│ │     else:                                                                                                          │ │
│ │         template = "ecommerce_default_planning.md"                                                                 │ │
│ │                                                                                                                    │ │
│ │     plan_response = generate_plan_with_claude(                                                                     │ │
│ │         template=template,                                                                                         │ │
│ │         context=state.issue_description                                                                            │ │
│ │     )                                                                                                              │ │
│ │                                                                                                                    │ │
│ │     state.complete_stage("plan", outputs={"plan_file": plan_response.file})                                        │ │
│ │                                                                                                                    │ │
│ │ # Blog project's planning stage                                                                                    │ │
│ │ # /blog-project/agentics/adws/adw_plan.py                                                                          │ │
│ │ def main():                                                                                                        │ │
│ │     adw_id = sys.argv[1]                                                                                           │ │
│ │     state = ADWState.load(adw_id)                                                                                  │ │
│ │                                                                                                                    │ │
│ │     # Blog specific planning logic                                                                                 │ │
│ │     if "cms" in state.issue_description.lower():                                                                   │ │
│ │         template = "blog_cms_planning.md"                                                                          │ │
│ │     elif "seo" in state.issue_description.lower():                                                                 │ │
│ │         template = "blog_seo_planning.md"                                                                          │ │
│ │     else:                                                                                                          │ │
│ │         template = "blog_content_planning.md"                                                                      │ │
│ │                                                                                                                    │ │
│ │     plan_response = generate_plan_with_claude(                                                                     │ │
│ │         template=template,                                                                                         │ │
│ │         context=state.issue_description                                                                            │ │
│ │     )                                                                                                              │ │
│ │                                                                                                                    │ │
│ │     state.complete_stage("plan", outputs={"plan_file": plan_response.file})                                        │ │
│ │                                                                                                                    │ │
│ │ ---                                                                                                                │ │
│ │ Phase 4: Project Templates & Configuration                                                                         │ │
│ │                                                                                                                    │ │
│ │ Project Configuration                                                                                              │ │
│ │                                                                                                                    │ │
│ │ // /client-project/agentics/adws/config.json                                                                       │ │
│ │ {                                                                                                                  │ │
│ │   "project_type": "ecommerce",                                                                                     │ │
│ │   "default_pipelines": {                                                                                           │ │
│ │     "feature": ["plan", "build", "security_scan", "test", "review"],                                               │ │
│ │     "bug": ["debug", "fix", "test"],                                                                               │ │
│ │     "chore": ["plan", "build"]                                                                                     │ │
│ │   },                                                                                                               │ │
│ │   "domain_keywords": {                                                                                             │ │
│ │     "payment": ["compliance_check", "security_audit"],                                                             │ │
│ │     "auth": ["security_scan", "penetration_test"],                                                                 │ │
│ │     "inventory": ["data_migration", "performance_test"]                                                            │ │
│ │   },                                                                                                               │ │
│ │   "custom_stages": [                                                                                               │ │
│ │     "security_scan",                                                                                               │ │
│ │     "compliance_check",                                                                                            │ │
│ │     "performance_test"                                                                                             │ │
│ │   ]                                                                                                                │ │
│ │ }                                                                                                                  │ │
│ │                                                                                                                    │ │
│ │ Template System                                                                                                    │ │
│ │                                                                                                                    │ │
│ │ /templates/                                                                                                        │ │
│ │ ├── ecommerce-template/                                                                                            │ │
│ │ │   └── agentics/adws/                                                                                             │ │
│ │ │       ├── adw_orchestrator.py      ← E-commerce optimized                                                        │ │
│ │ │       ├── adw_security_scan.py     ← Domain-specific stages                                                      │ │
│ │ │       ├── adw_compliance_check.py                                                                                │ │
│ │ │       └── config.json              ← E-commerce defaults                                                         │ │
│ │ │                                                                                                                  │ │
│ │ ├── blog-template/                                                                                                 │ │
│ │ │   └── agentics/adws/                                                                                             │ │
│ │ │       ├── adw_orchestrator.py      ← Blog optimized                                                              │ │
│ │ │       ├── adw_seo_check.py         ← Blog-specific stages                                                        │ │
│ │ │       ├── adw_content_review.py                                                                                  │ │
│ │ │       └── config.json              ← Blog defaults                                                               │ │
│ │ │                                                                                                                  │ │
│ │ └── api-template/                                                                                                  │ │
│ │     └── agentics/adws/                                                                                             │ │
│ │         ├── adw_orchestrator.py      ← API optimized                                                               │ │
│ │         ├── adw_load_test.py         ← API-specific stages                                                         │ │
│ │         ├── adw_security_audit.py                                                                                  │ │
│ │         └── config.json              ← API defaults                                                                │ │
│ │                                                                                                                    │ │
│ │ ---                                                                                                                │ │
│ │ Phase 5: Enhanced UI Features                                                                                      │ │
│ │                                                                                                                    │ │
│ │ Multi-Project Workspace                                                                                            │ │
│ │                                                                                                                    │ │
│ │ // Project tabs like VS Code                                                                                       │ │
│ │ const ProjectTabs = () => {                                                                                        │ │
│ │   const { projects, currentProject, selectProject } = useKanbanStore();                                            │ │
│ │                                                                                                                    │ │
│ │   return (                                                                                                         │ │
│ │     <div className="project-tabs">                                                                                 │ │
│ │       {projects.map(project => (                                                                                   │ │
│ │         <Tab                                                                                                       │ │
│ │           key={project.path}                                                                                       │ │
│ │           active={project.path === currentProject}                                                                 │ │
│ │           onClick={() => selectProject(project.path)}                                                              │ │
│ │         >                                                                                                          │ │
│ │           {project.name}                                                                                           │ │
│ │           <TabContent>                                                                                             │ │
│ │             <TaskBoard projectPath={project.path} />                                                               │ │
│ │           </TabContent>                                                                                            │ │
│ │         </Tab>                                                                                                     │ │
│ │       ))}                                                                                                          │ │
│ │     </div>                                                                                                         │ │
│ │   );                                                                                                               │ │
│ │ };                                                                                                                 │ │
│ │                                                                                                                    │ │
│ │ Rich Task Creation                                                                                                 │ │
│ │                                                                                                                    │ │
│ │ const TaskCreationForm = () => {                                                                                   │ │
│ │   const [taskData, setTaskData] = useState({                                                                       │ │
│ │     title: "",                                                                                                     │ │
│ │     description: "",                                                                                               │ │
│ │     work_item_type: "feature",                                                                                     │ │
│ │     images: [],                                                                                                    │ │
│ │     selected_stages: [] // Optional override                                                                       │ │
│ │   });                                                                                                              │ │
│ │                                                                                                                    │ │
│ │   const projectConfig = useProjectConfig(); // Load from project's config.json                                     │ │
│ │                                                                                                                    │ │
│ │   return (                                                                                                         │ │
│ │     <form onSubmit={handleSubmit}>                                                                                 │ │
│ │       <RichTextEditor                                                                                              │ │
│ │         value={taskData.description}                                                                               │ │
│ │         onChange={(desc) => setTaskData({...taskData, description: desc})}                                         │ │
│ │         supportImages={true}                                                                                       │ │
│ │         supportAnnotations={true}                                                                                  │ │
│ │       />                                                                                                           │ │
│ │                                                                                                                    │ │
│ │       <StageSelector                                                                                               │ │
│ │         availableStages={projectConfig.custom_stages}                                                              │ │
│ │         defaultPipeline={projectConfig.default_pipelines[taskData.work_item_type]}                                 │ │
│ │         onSelectionChange={(stages) => setTaskData({...taskData, selected_stages: stages})}                        │ │
│ │       />                                                                                                           │ │
│ │     </form>                                                                                                        │ │
│ │   );                                                                                                               │ │
│ │ };                                                                                                                 │ │
│ │                                                                                                                    │ │
│ │ ---                                                                                                                │ │
│ │ Benefits of This Architecture                                                                                      │ │
│ │                                                                                                                    │ │
│ │ 1. Project Intelligence                                                                                            │ │
│ │                                                                                                                    │ │
│ │ - E-commerce: Knows about payments, security, compliance                                                           │ │
│ │ - Blog: Knows about CMS, SEO, content workflows                                                                    │ │
│ │ - API: Knows about load testing, documentation, versioning                                                         │ │
│ │ - Mobile: Knows about device testing, app stores                                                                   │ │
│ │                                                                                                                    │ │
│ │ 2. Kanban Simplicity                                                                                               │ │
│ │                                                                                                                    │ │
│ │ // Kanban's responsibilities:                                                                                      │ │
│ │ ✅ Send task data to project                                                                                        │ │
│ │ ✅ Watch state files for changes                                                                                    │ │
│ │ ✅ Display progress visually                                                                                        │ │
│ │ ✅ Provide controls (kill, retry)                                                                                   │ │
│ │                                                                                                                    │ │
│ │ // NOT responsible for:                                                                                            │ │
│ │ ❌ Deciding workflow order                                                                                          │ │
│ │ ❌ Knowing domain-specific logic                                                                                    │ │
│ │ ❌ Managing stage execution                                                                                         │ │
│ │ ❌ Understanding project types                                                                                      │ │
│ │                                                                                                                    │ │
│ │ 3. Scalability                                                                                                     │ │
│ │                                                                                                                    │ │
│ │ - New project types = new templates                                                                                │ │
│ │ - New stages = add to project's adws/ folder                                                                       │ │
│ │ - Custom workflows = modify project's orchestrator                                                                 │ │
│ │ - Domain expertise = embed in project templates                                                                    │ │
│ │                                                                                                                    │ │
│ │ 4. Developer Experience                                                                                            │ │
│ │                                                                                                                    │ │
│ │ - Familiar: Like VS Code's project-centric approach                                                                │ │
│ │ - Customizable: Each project can define its own workflows                                                          │ │
│ │ - Reusable: Templates provide domain-specific starting points                                                      │ │
│ │ - Transparent: All logic visible in project's adws/ folder                                                         │ │
│ │                                                                                                                    │ │
│ │ This architecture makes the Kanban board a universal tool while keeping domain intelligence where it belongs - in  │ │
│ │ each project's codebase.                                                                                           │ │
│ ╰───────────────────────────────────────────────────────────────────────────────────────────────────────