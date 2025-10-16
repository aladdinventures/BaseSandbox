document.addEventListener("DOMContentLoaded", () => {
    fetchData();
});

async function fetchData() {
    try {
        const response = await fetch("data/dashboard_data.json");
        const data = await response.json();
        renderDashboard(data);
    } catch (error) {
        console.error("Error fetching dashboard data:", error);
        document.getElementById("overall-status-text").textContent = "خطا در بارگذاری داده‌ها";
        document.getElementById("overall-status").classList.add("failed");
    }
}

function renderDashboard(data) {
    const overallStatusElement = document.getElementById("overall-status-text");
    const overallStatusCard = document.getElementById("overall-status");
    const projectListElement = document.getElementById("project-list");

    overallStatusElement.textContent = data.overall_status;
    if (data.overall_status.includes("موفق")) {
        overallStatusCard.classList.add("success");
    } else if (data.overall_status.includes("ناموفق")) {
        overallStatusCard.classList.add("failed");
    } else {
        overallStatusCard.classList.add("unknown");
    }

    projectListElement.innerHTML = ""; // Clear previous content

    for (const projectName in data.projects) {
        const project = data.projects[projectName];
        const projectCard = document.createElement("div");
        projectCard.classList.add("project-card");

        let overallProjectStatusClass = "نامشخص";
        if (project.status && project.status.includes("موفق")) {
            overallProjectStatusClass = "موفق";
        } else if (project.status && project.status.includes("ناموفق")) {
            overallProjectStatusClass = "ناموفق";
        }

        projectCard.innerHTML = `
            <h3>${projectName} <span class="status-badge ${overallProjectStatusClass}">${project.status || 'نامشخص'}</span></h3>
            <p><strong>وضعیت بیلد:</strong> <span class="status-badge ${project.build_status === 'موفق' ? 'موفق' : 'ناموفق'}">${project.build_status || 'نامشخص'}</span></p>
            <p><strong>وضعیت تست:</strong> <span class="status-badge ${project.test_status === 'موفق' ? 'موفق' : 'ناموفق'}">${project.test_status || 'نامشخص'}</span></p>
            <p><strong>وضعیت استقرار:</strong> <span class="status-badge ${project.deploy_status === 'موفق' ? 'موفق' : 'ناموفق'}">${project.deploy_status || 'نامشخص'}</span></p>
            <p><strong>مدت زمان اجرا:</strong> ${project.duration || 'نامشخص'}</p>
            <div class="log-section">
                <h4>لاگ بیلد:</h4>
                <pre>${project.build_log || 'لاگی موجود نیست.'}</pre>
            </div>
            <div class="log-section">
                <h4>لاگ تست:</h4>
                <pre>${project.test_log || 'لاگی موجود نیست.'}</pre>
            </div>
            <div class="log-section">
                <h4>لاگ استقرار:</h4>
                <pre>${project.deploy_log || 'لاگی موجود نیست.'}</pre>
            </div>
        `;
        projectListElement.appendChild(projectCard);
    }
}

