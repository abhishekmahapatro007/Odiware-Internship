---

### Step-by-Step Process to Track Material Usage by Site in Odoo

#### **Step 1: Enable Multi-Site Operations**
1. **Create Warehouses for Each Site:**
   - Navigate to **Inventory > Configuration > Warehouses**.
   - Click on **Create** to add a new warehouse for each construction site (e.g., "Site A", "Site B").
   - This will allow you to track inventory separately for each site.

2. **(Optional) Set Up Locations Within Warehouses:**
   - If needed, go to **Inventory > Configuration > Locations**.
   - You can add specific locations for each warehouse to track materials more precisely within different parts of the site.

---

#### **Step 2: Set Up Budgeting (Optional for Cost Tracking)**
1. **Create Analytic Accounts for Sites:**
   - Go to **Accounting > Configuration > Analytic Accounts**.
   - Create one analytic account for each site (e.g., "Site A Budget", "Site B Budget").
   - This allows you to track costs separately for each site.

2. **Link Purchases and Expenses to Analytic Accounts:**
   - When entering a purchase order or recording an expense, ensure the transaction is linked to the corresponding **Analytic Account** for the site.

---

#### **Step 3: Customize Inventory Reports for Site-Specific Material Consumption**
1. **Create a Report Template for Material Consumption by Site:**
   - You will need to either use **Odoo Studio** or go to **Settings > Technical > Reports** to create a new report.
   - This report will aggregate the material usage for each warehouse (representing the construction site).
   - You can filter the report by **Warehouse** to show data for each site.

2. **Include Material Usage Data:**
   - For the report, include the **Material (Product)** and **Quantity Consumed** columns.
   - The report should sum up material usage based on the warehouse (site).

3. **Add a Menu Item for Easy Access:**
   - To make it easier for site managers to generate reports, add a custom menu item under **Inventory > Reporting** that links to the new report.

---

#### **Step 4: Create Dashboards for Site Managers**
1. **Create a Dashboard for Material Usage Monitoring:**
   - Use **Odoo Studio** to create a new **Dashboard** for site managers.
   - Add **Widgets** such as **Bar Graphs** or **Pie Charts** to visualize material usage per site.
     - For example, a bar graph showing the total material consumption for each site.

2. **Assign the Dashboard to Site Managers:**
   - Navigate to **Settings > Users & Companies > Users**.
   - Ensure that site managers have access to the dashboard by assigning them the appropriate user role.

---

#### **Step 5: Generate Material Usage Reports**
1. **Generate Site-Specific Reports:**
   - Site managers can now go to the **Inventory Reporting** menu and select the **Material Usage Report**.
   - The report will show material usage broken down by warehouse (site).
   
2. **Filter by Site:**
   - Use the report filters to select specific sites (warehouses) and view material consumption for those locations.

3. **Export Data if Needed:**
   - If required, you can allow the report to be exported as a **CSV** or **Excel file** for offline analysis or integration with other systems.

---

#### **Step 6: (Optional) Set Up Alerts for Budget Overruns**
1. **Create Automated Alerts:**
   - Use **Automated Actions** in Odoo to create alerts for site managers when material consumption exceeds the budgeted amount for a site.
   - For example, set a threshold to trigger a notification if the material consumption for a site exceeds a predefined limit.

---

### **Conclusion:**
This process will enable you to manage material usage for multiple construction sites within Odoo, providing detailed reports and dashboards to site managers. You will also have the option to track site-specific budgets and set up alerts if material consumption goes beyond set thresholds.

By following these steps, site managers will have a clear view of the materials used at each construction site, helping them optimize inventory, track spending, and make better decisions on-site management.
