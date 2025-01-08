## 3.1 Project Management 
In Odoo, the **Project Management module** allows you to plan, track, and manage construction projects, such as building highways, by organizing tasks, setting budgets, and 
visualizing timelines. Below is a step-by-step guide on how to configure and manage a highway construction project in Odoo.

### 1. **Configure the Project Module**

#### a. Install the Project Management Module:
1. Go to the **Apps** menu in Odoo.
2. Search for the **Project** app.
3. Click **Install** to activate the project management functionality.

#### b. Create a New Project:
1. Go to the **Project** app.
2. Click on **Create** to create a new project.
3. Name your project: e.g., **Highway Construction Project**.
4. (Optional) Define the **Customer** if this project is customer-facing or for an external party (this can be left blank for internal projects).
5. Set the **Project Type** (e.g., Internal Project or Customer Project).
6. Save the project.

### 2. **Define Tasks, Subtasks, and Milestones**

#### a. Create Tasks:
In Odoo, tasks represent the main steps or phases in a project. 

1. **Navigate to the Project Dashboard** and select your **Highway Construction Project**.
2. Click on **Add a Task** to create a new task.

   For example, create tasks like:
   - **Site Preparation**
   - **Material Procurement**
   - **Construction Phase 1: Earthworks**
   - **Construction Phase 2: Pavement**
   - **Construction Phase 3: Signage and Finishing**

3. After creating each task, you can **assign responsible people**, set deadlines, and link tasks to milestones.
4. You can break down the tasks into **subtasks** by opening each task and clicking on the **Subtasks** tab to create specific items under each major task.

   Example for **Site Preparation**:
   - Subtask 1: **Land Survey**
   - Subtask 2: **Clearing Vegetation**
   - Subtask 3: **Leveling Ground**

#### b. Set Milestones:
Milestones help track major project achievements.

1. In Odoo, milestones are typically represented by specific tasks that mark critical project points.
2. You can create a milestone task, for example:
   - **Milestone 1**: Site Preparation Complete (linked to the completion of Site Preparation task)
   - **Milestone 2**: Material Procurement Complete
   - **Milestone 3**: Earthworks Complete
   - **Milestone 4**: Pavement Complete
   - **Milestone 5**: Project Completed

**Tip:** Milestones do not have detailed tasks associated with them but act as project checkpoints to monitor progress.

### 3. **Set Up Budgets and Link Them to Tasks**

#### a. Enable Budgeting:
1. Go to the **Accounting** app, and make sure you have **Analytic Accounting** enabled. This allows you to set up budgets for projects and track their costs.
2. Navigate to **Configuration > Settings** in the Accounting app, and ensure that **Analytic Accounting** is activated.

#### b. Create a Budget for the Project:
1. Open your **Highway Construction Project**.
2. In the project view, you will find an option for **Budget** under the "Project" or "Expenses" tab.
3. Define the **overall budget** for the project and allocate it to each task. For example:
   - **Site Preparation**: $50,000
   - **Material Procurement**: $150,000
   - **Earthworks**: $200,000
   - **Pavement**: $300,000
   - **Signage and Finishing**: $50,000
   - **Total Budget**: $750,000

#### c. Link Budget to Tasks:
1. Open each task (e.g., **Site Preparation**).
2. In the task’s form view, you can assign **analytic accounts** for budgeting and cost tracking. You may need to set up these analytic accounts in the **Accounting** module first if they are not already created.
3. Set the **estimated costs** for each task (e.g., costs for materials, resources, labor) under the **Budget** section.

### 4. **Enable Gantt Charts and Timelines for Visual Tracking**

#### a. View Project Timeline with Gantt Charts:
1. Navigate to the **Project** app.
2. Open your **Highway Construction Project**.
3. On the project’s dashboard, switch to the **Gantt View** (found in the top-right corner of the project view).
4. The Gantt chart will display all the tasks along a timeline, showing their start and end dates.
   
   - Tasks like **Site Preparation**, **Material Procurement**, and **Construction Phases** will appear as bars on the chart, with task dependencies and the overall project timeline visually represented.
   
   - You can adjust the dates for each task by dragging the task bars in the Gantt chart.
   - Task progress will also be shown visually, so you can track whether tasks are on schedule, delayed, or completed.

#### b. Monitor Task Dependencies:
1. In the **Gantt View**, you can set **dependencies** between tasks (e.g., "Material Procurement" must be completed before "Construction Phase 1: Earthworks" begins).
2. To add dependencies:
   - Click on a task in the Gantt chart, then click on the **Link** button to link it to another task.

#### c. Adjust and Track Progress:
- The Gantt chart will automatically update as tasks are marked complete or delayed, making it easier to visualize whether the project is on track.

### 5. **Scenario: Highway Construction Project**

Here’s an example scenario you could implement:

#### Project: **Highway Construction Project**

   **1. Tasks and Subtasks:**
   - **Site Preparation**
     - Subtask 1.1: Land Survey (Start Date: Jan 15, End Date: Jan 22)
     - Subtask 1.2: Clearing Vegetation (Start Date: Jan 23, End Date: Jan 30)
     - Subtask 1.3: Leveling Ground (Start Date: Jan 31, End Date: Feb 5)
     - **Milestone**: Site Preparation Complete (Date: Feb 5)

   - **Material Procurement**
     - Subtask 2.1: Research Suppliers (Start Date: Jan 10, End Date: Jan 15)
     - Subtask 2.2: Purchase Materials (Start Date: Jan 16, End Date: Jan 22)
     - Subtask 2.3: Transport Materials (Start Date: Jan 23, End Date: Feb 2)
     - **Milestone**: Materials Procurement Complete (Date: Feb 2)

   - **Construction Phase 1 (Earthworks)**
     - Subtask 3.1: Excavation (Start Date: Feb 6, End Date: Feb 15)
     - Subtask 3.2: Foundation Setting (Start Date: Feb 16, End Date: Feb 25)
     - **Milestone**: Earthworks Complete (Date: Feb 25)

   - **Construction Phase 2 (Pavement)**
     - Subtask 4.1: Paving Road (Start Date: Feb 26, End Date: Mar 10)
     - **Milestone**: Pavement Complete (Date: Mar 10)

   - **Construction Phase 3 (Signage and Finishing)**
     - Subtask 5.1: Install Signs (Start Date: Mar 11, End Date: Mar 20)
     - Subtask 5.2: Final Touches (Start Date: Mar 21, End Date: Mar 25)
     - **Milestone**: Project Completed (Date: Mar 25)

#### Budget:
   - **Total Project Budget**: $750,000
   - Break down the budget by task and subtask (as explained earlier).

#### Gantt Chart:
   - You’ll be able to visualize all tasks and their dependencies, tracking progress along the timeline.

By following these steps in Odoo, you will have successfully set up the **Highway Construction Project**, including task management, budgeting, and visual tracking via the Gantt chart.

.
--
## 3.3 Inventory Management
To effectively manage **inventory** across a **central warehouse** and **multiple construction sites** in **Odoo**, you need to set up your system to track **materials**, 
**transfers**, and **consumption**. The key tasks involve configuring warehouses, stock locations, inter-site stock transfers, consumption tracking, and batch tracking for 
materials. Here’s a step-by-step guide on how to set this up in Odoo.

### 1. **Configure Warehouses for the Central Store and Site-Specific Inventories**

You will need to set up **multiple warehouses** in Odoo for both your **central warehouse** and each **construction site**.

#### Step 1: Enable the Multi-Warehouse Feature
   - **Step 1**: Go to **Settings** in Odoo.
   - **Step 2**: Under the **Inventory** section, enable **"Multi-Warehouse"** functionality.
   - **Step 3**: Save the changes. This allows you to manage more than one warehouse.

#### Step 2: Create Warehouses for Central and Sites
   - **Step 1**: Go to the **Inventory** app.
   - **Step 2**: Navigate to **Configuration** > **Warehouses**.
   - **Step 3**: Click on **Create** to add a new warehouse.
   - **Step 4**: For each warehouse:
     - **Name** the warehouse (e.g., "Central Warehouse", "Site 1 Warehouse", "Site 2 Warehouse").
     - Assign the **company** if needed (in case of multi-company setup).
     - Configure specific **operating locations** (receiving, stock, delivery) for each warehouse.

#### Step 3: Configure Warehouse-Specific Settings
   - **Step 1**: For each warehouse, configure the **internal locations** where materials will be stored (such as raw materials, tools, spare parts, etc.).
   - **Step 2**: You can customize the **locations** for each warehouse (this is useful for organizing materials on-site or in the central warehouse).

### 2. **Set Up Stock Locations Within Each Warehouse (Raw Materials, Tools, Spare Parts)**

Now, define the specific **stock locations** within each warehouse to organize your inventory.

#### Step 1: Define Locations for Each Warehouse
   - **Step 1**: Go to **Inventory** > **Configuration** > **Locations**.
   - **Step 2**: Click **Create** to add a new stock location.
   - **Step 3**: Assign each location a name based on the type of materials you plan to store (e.g., **Raw Materials**, **Tools**, **Spare Parts**, etc.).
   - **Step 4**: For each location, select the **parent warehouse** (Central Warehouse or any Site Warehouse).
   - **Step 5**: Define if the location is **internal**, **supplier** (for incoming goods), or **customer** (for outgoing goods).

#### Step 2: Organize Locations Based on Material Type
   - Create different stock locations for materials at the **central warehouse** and each **construction site**. For example:
     - **Central Warehouse**: Raw Materials, Tools, Spare Parts.
     - **Site 1 Warehouse**: Raw Materials, Consumables.
     - **Site 2 Warehouse**: Raw Materials, Equipment.
   - This will help in easily tracking and managing the materials at each location.

### 3. **Test Inter-Site Stock Transfers and Consumption Tracking**

You need to ensure that materials can be transferred between warehouses and tracked properly when used on-site.

#### Step 1: Set Up Inter-Site Stock Transfers
   - **Step 1**: Go to **Inventory** > **Operations** > **Transfers**.
      - Receipts when you are receiving products into inventory.
      - Deliver the products to customers, go to Inventory > Operations > Deliveries.
      - If you are moving products between internal locations (e.g., warehouse to store), go to Inventory > Operations > Internal Transfers.
   - **Step 2**: Click on **Create** to initiate a new transfer.
   - **Step 3**: Choose the **source warehouse** (e.g., Central Warehouse) and **destination warehouse** (e.g., Site 1 Warehouse).
   - **Step 4**: Add the materials to be transferred. This could be cement, steel, tools, etc.
   - **Step 5**: Confirm and validate the transfer. Once confirmed, the stock quantities will be updated in the destination warehouse.

#### Step 2: Track Consumption at the Site
   - **Step 1**: When materials are consumed on-site, go to **Inventory** > **Operations** > **Consumption**.
   - **Step 2**: Record the consumption of materials from each site warehouse (e.g., Site 1 Warehouse).
   - **Step 3**: Enter the materials consumed (e.g., cement bags used for the project).
   - **Step 4**: Save and confirm the consumption record. This will update the stock levels at the site warehouse.

#### Step 3: Test Material Transfer and Consumption
   - **Step 1**: Test the flow by performing the following:
     - Create a **stock transfer** from the **Central Warehouse** to **Site 1**.
     - Track **material consumption** on-site by logging material usage.
   - **Step 2**: Ensure that stock quantities at both the source and destination warehouses are updated correctly.

### 4. **Enable Batch Tracking for Materials with Expiration Dates (e.g., Cement Bags)**

For materials like **cement** that have **expiration dates**, Odoo provides a feature called **batch tracking** to manage stock efficiently.

#### Step 1: Enable Lot/Serial Numbers and Expiration Tracking
   - **Step 1**: Go to **Inventory** > **Configuration** > **Settings**.
   - **Step 2**: Under the **Traceability** section, enable the **"Tracking by Lot or Serial Number"** option.
   - **Step 3**: Enable **Expiration Date Tracking** for products that have a shelf life (e.g., cement).
   - **Step 4**: Save the settings.

#### Step 2: Set Expiration Dates for Products
   - **Step 1**: Go to **Inventory** > **Products**.
   - **Step 2**: Select the product (e.g., **Cement**).
   - **Step 3**: In the product form, go to the **Inventory** tab and ensure that **lot tracking** and **expiration date tracking** are enabled for that product.
   - **Step 4**: Set a **specific expiration date** for the batch of materials (e.g., cement bags with expiration dates).

#### Step 3: Use Batch Numbers During Stock Movements
   - **Step 1**: When you create a transfer or stock consumption, you’ll be prompted to select the **lot number** or **batch number**.
   - **Step 2**: Ensure that you select the correct batch when transferring or consuming materials, and Odoo will automatically manage the expiration dates for you.

#### Step 4: Track Expiration and Manage FIFO
   - **Step 1**: Regularly monitor products with expiration dates using Odoo’s **Inventory Reports**.
   - **Step 2**: You can use FIFO (First In, First Out) or other methods to ensure that the oldest stock is used first.

### Example Scenario: Track Material Transfers and Consumption During the Project

#### Transfer Material from Central Warehouse to Site:
- A **purchase order** is placed for **cement** to the central warehouse.
- A **stock transfer** is created to move the cement from the **Central Warehouse** to **Site 1 Warehouse**.
- Once transferred, the cement stock is now available for consumption at the site.

#### Consume Material at the Site:
- As construction progresses, cement is consumed from the **Site 1 Warehouse**.
- **Consumption records** are created to reflect the amount of cement used in the project.
- The stock levels are updated, and **traceability** ensures that the exact batch of cement used is logged for future reference.

#### Manage Expiring Material:
- If a batch of cement is nearing its expiration date, Odoo can automatically notify you to use the stock before it expires.
- You can prioritize consuming the **earlier batch** first to avoid wastage.

---

### Conclusion:

By following the above steps, you can set up Odoo for **inventory management** at the **central warehouse** and **construction sites**, ensuring accurate tracking of material **transfers**, **consumption**, and **expiration dates**. With proper setup, you will streamline operations, reduce errors, and improve project material management.

--

