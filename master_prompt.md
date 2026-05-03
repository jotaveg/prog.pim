**Role:** You are an expert Full-Stack Python Developer specializing in Django and Rapid Prototyping (MVP development).

**Project Objective:** Build a "Sistema Colaborativo Acadêmico" (Academic Collaborative System). The goal is a functional MVP for a school project that demonstrates user authentication, role-based access, and data management.

**Technical Stack:**

- **Backend:** Python 3.x with **Django Framework**.
    
- **Database:** **SQLite** (pre-configured with Django).
    
- **Frontend:** HTML5 with **Tailwind CSS** (via CDN for simplicity).
    
- **Auth:** Django’s built-in `User` and `Group` system.
    

**Architectural Requirements:**

1. **UI/UX:** Use a **Header-only navigation** (Top Nav). Do not use sidebars. Ensure the design is clean and "academic."
    
2. **User Roles:** Implement a simple hierarchy: **Administrator** (Full access), **Professor** (Manage content/tasks), and **Student** (View/Submit/Collaborate).
    
3. **Pages (Minimum 5):**
    
    - **Landing/Login Page:** Basic entry point.
        
    - **Dashboard:** Personalized view based on role.
        
    - **Project/Class List:** View all collaborative groups.
        
    - **Project Detail:** The workspace for collaboration.
        
    - **Profile/Settings:** User info display.
        
4. **Data Logic:** Provide a `management/commands` script or a `utils.py` function to populate the SQLite database with mock data (Users, Projects, Posts) for demonstration purposes.
    

**Task Instructions:**

1. Outline the `models.py` including a `Project` and `Task/Post` model linked to the User roles.
    
2. Provide the `views.py` using Django’s Class-Based Views for speed.
    
3. Generate a base HTML template with a Tailwind Header and a content block.
    
4. Provide the mock data generation script.
    
5. Keep the logic "Plug-and-Play"—prioritize built-in Django features over custom complex logic.