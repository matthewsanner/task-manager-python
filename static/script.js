document.addEventListener("DOMContentLoaded", function () {
  const taskList = document.getElementById("taskList");
  const taskForm = document.getElementById("taskForm");
  const sortOptions = document.getElementById("sortOptions");
  const searchBox = document.getElementById("searchBox");

  // Fetch and display all tasks on load
  loadTasks();

  function loadTasks() {
    fetch("/api/tasks")
      .then((response) => response.json())
      .then((data) => {
        displayTasks(data);
      })
      .catch((error) => console.error("Error loading tasks:", error));
  }

  function loadSortedTasks(sortBy) {
    fetch(`/api/tasks/sorted?sort_by=${sortBy}`)
      .then((response) => response.json())
      .then((data) => {
        displayTasks(data);
      })
      .catch((error) => console.error("Error loading sorted tasks:", error));
  }

  function loadFoundTasks(query) {
    fetch(`/api/tasks/search?query=${query}`)
      .then((response) => response.json())
      .then((data) => {
        displayTasks(data);
      })
      .catch((error) => console.error("Error loading found tasks:", error));
  }

  function displayTasks(tasks) {
    taskList.innerHTML = "";
    tasks.forEach((task) => {
      const li = document.createElement("li");
      li.innerHTML = `
                    <strong>${task.title}</strong> - ${task.description} (Due: ${task.due_date}, Priority: ${task.priority})
                    <button class="complete-btn" data-id="${task.id}">Complete</button>
                    <button class="delete-btn" data-id="${task.id}">Delete</button>
                `;
      if (task.completed) {
        li.style.textDecoration = "line-through";
      }
      taskList.appendChild(li);
    });
  }

  // Handle form submission
  taskForm.addEventListener("submit", function (event) {
    event.preventDefault();
    const title = document.getElementById("title").value;
    const description = document.getElementById("description").value;
    const due_date = document.getElementById("due_date").value;
    const priority = document.getElementById("priority").value;

    fetch("/api/tasks", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ title, description, due_date, priority }),
    })
      .then((response) => response.json())
      .then(() => {
        taskForm.reset();
        loadTasks();
      })
      .catch((error) => console.error("Error adding task:", error));
  });

  sortOptions.addEventListener("change", function () {
    const selectedSort = sortOptions.value;
    if (selectedSort === "priority" || selectedSort === "due_date") {
      loadSortedTasks(selectedSort);
    } else {
      loadTasks();
    }
  });

  searchBox.addEventListener("submit", function (event) {
    event.preventDefault();
    const query = document.getElementById("query").value;

    if (query) {
      loadFoundTasks(query);
    } else {
      loadTasks();
    }
  });

  // Event delegation for task actions
  taskList.addEventListener("click", function (event) {
    if (event.target.classList.contains("complete-btn")) {
      const taskId = event.target.getAttribute("data-id");
      markComplete(taskId);
    } else if (event.target.classList.contains("delete-btn")) {
      const taskId = event.target.getAttribute("data-id");
      deleteTask(taskId);
    }
  });

  function markComplete(taskId) {
    fetch(`/api/tasks/${taskId}`, {
      method: "PUT",
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error("Failed to mark task as complete");
        }
        return response.json();
      })
      .then(() => {
        loadTasks();
      })
      .catch((error) => console.error("Error completing task:", error));
  }

  function deleteTask(taskId) {
    fetch(`/api/tasks/${taskId}`, {
      method: "DELETE",
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error("Failed to delete task");
        }
        return response.json();
      })
      .then(() => {
        loadTasks();
      })
      .catch((error) => console.error("Error deleting task:", error));
  }
});
