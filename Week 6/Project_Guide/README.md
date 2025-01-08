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

