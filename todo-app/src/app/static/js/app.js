// Todo App JavaScript

// Theme toggle
function toggleTheme() {
    const body = document.body;
    const icon = document.querySelector('#theme-toggle sl-icon');

    if (body.classList.contains('sl-theme-light')) {
        body.classList.remove('sl-theme-light');
        body.classList.add('sl-theme-dark');
        icon.name = 'sun';
        localStorage.setItem('theme', 'dark');
    } else {
        body.classList.remove('sl-theme-dark');
        body.classList.add('sl-theme-light');
        icon.name = 'moon';
        localStorage.setItem('theme', 'light');
    }
}

// Initialize theme from localStorage
document.addEventListener('DOMContentLoaded', () => {
    const savedTheme = localStorage.getItem('theme');
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    const icon = document.querySelector('#theme-toggle sl-icon');

    if (savedTheme === 'dark' || (!savedTheme && prefersDark)) {
        document.body.classList.remove('sl-theme-light');
        document.body.classList.add('sl-theme-dark');
        if (icon) icon.name = 'sun';
    }
});

// Initialize SortableJS for list reordering (sidebar)
function initListSortable() {
    const sidebarLists = document.getElementById('sidebar-lists');
    if (sidebarLists && typeof Sortable !== 'undefined') {
        new Sortable(sidebarLists, {
            animation: 150,
            handle: '.drag-handle',
            ghostClass: 'sortable-ghost',
            chosenClass: 'sortable-chosen',
            dragClass: 'sortable-drag',
            filter: '.empty-sidebar',
            onEnd: function() {
                htmx.trigger(sidebarLists, 'end');
            }
        });
    }
}

// Initialize SortableJS for todo reordering
function initTodoSortable() {
    const todosList = document.getElementById('todos-list');
    if (todosList && typeof Sortable !== 'undefined') {
        new Sortable(todosList, {
            animation: 150,
            handle: '.todo-drag-handle',
            ghostClass: 'sortable-ghost',
            chosenClass: 'sortable-chosen',
            dragClass: 'sortable-drag',
            onEnd: function(evt) {
                // Get the todo ID and new position
                const todoId = evt.item.dataset.todoId;
                const newPosition = evt.newIndex;

                // Send position update to server
                htmx.ajax('POST', `/api/todos/${todoId}/reorder`, {
                    values: { position: newPosition },
                    swap: 'none'
                });
            }
        });
    }
}

function initSortable() {
    initListSortable();
    initTodoSortable();
}

document.addEventListener('DOMContentLoaded', initSortable);

// Re-initialize sortable after HTMX swaps
document.body.addEventListener('htmx:afterSwap', (evt) => {
    if (evt.detail.target.id === 'sidebar-lists') {
        initListSortable();
    }
    if (evt.detail.target.id === 'todos-list' || evt.detail.target.id === 'main-content') {
        initTodoSortable();
    }
});

// Edit list dialog - uses data attributes for XSS safety
function openEditListDialog(id, name, description, color) {
    const dialog = document.getElementById('edit-list-dialog');
    const form = document.getElementById('edit-list-form');

    document.getElementById('edit-list-name').value = name;
    document.getElementById('edit-list-description').value = description;
    document.getElementById('edit-list-color').value = color;

    form.setAttribute('hx-put', `/api/lists/${id}`);
    form.setAttribute('hx-target', `#list-${id}`);
    htmx.process(form);

    dialog.show();
}

// Edit todo dialog - uses data attributes for XSS safety
function openEditTodoDialog(id, title, note, dueDate, priority) {
    const dialog = document.getElementById('edit-todo-dialog');
    const form = document.getElementById('edit-todo-form');

    document.getElementById('edit-todo-title').value = title;
    document.getElementById('edit-todo-note').value = note;
    document.getElementById('edit-todo-due-date').value = dueDate;
    document.getElementById('edit-todo-priority').value = priority;

    form.setAttribute('hx-put', `/api/todos/${id}`);
    form.setAttribute('hx-target', `#todo-${id}`);
    htmx.process(form);

    dialog.show();
}

// Delete confirmations
let pendingDelete = null;

function confirmDeleteList(id, name) {
    const dialog = document.getElementById('delete-confirm-dialog');
    const message = document.getElementById('delete-confirm-message');

    message.textContent = `Are you sure you want to delete "${name}"? All todos in this list will also be deleted.`;

    pendingDelete = {
        type: 'list',
        id: id
    };

    dialog.show();
}

function confirmDeleteTodo(id, title) {
    const dialog = document.getElementById('delete-confirm-dialog');
    const message = document.getElementById('delete-confirm-message');

    message.textContent = `Are you sure you want to delete "${title}"?`;

    pendingDelete = {
        type: 'todo',
        id: id
    };

    dialog.show();
}

// Event delegation for dynamic elements
document.addEventListener('DOMContentLoaded', () => {
    // Handle delete confirmation button
    const confirmBtn = document.getElementById('delete-confirm-btn');
    if (confirmBtn) {
        confirmBtn.addEventListener('click', () => {
            if (!pendingDelete) return;

            const url = pendingDelete.type === 'list'
                ? `/api/lists/${pendingDelete.id}`
                : `/api/todos/${pendingDelete.id}`;

            htmx.ajax('DELETE', url, {
                target: pendingDelete.type === 'list' ? '#main-content' : `#todo-${pendingDelete.id}`,
                swap: pendingDelete.type === 'list' ? 'innerHTML' : 'delete'
            });

            document.getElementById('delete-confirm-dialog').hide();
            pendingDelete = null;
        });
    }

    // Helper function to handle button clicks (works with Shadow DOM)
    function handleIconButtonClick(selector, handler) {
        document.querySelectorAll(selector).forEach(btn => {
            btn.addEventListener('click', handler);
        });
    }

    // Initialize button handlers
    function initButtonHandlers() {
        // Todo edit buttons
        handleIconButtonClick('.edit-todo-btn', function(e) {
            e.stopPropagation();
            const todoItem = this.closest('.todo-item');
            if (todoItem) {
                openEditTodoDialog(
                    todoItem.dataset.todoId,
                    todoItem.dataset.todoTitle,
                    todoItem.dataset.todoNote,
                    todoItem.dataset.todoDueDate,
                    todoItem.dataset.todoPriority
                );
            }
        });

        // Todo delete buttons
        handleIconButtonClick('.delete-todo-btn', function(e) {
            e.stopPropagation();
            const todoItem = this.closest('.todo-item');
            if (todoItem) {
                confirmDeleteTodo(
                    todoItem.dataset.todoId,
                    todoItem.dataset.todoTitle
                );
            }
        });

        // List edit buttons (sidebar)
        handleIconButtonClick('.edit-list-btn', function(e) {
            e.stopPropagation();
            const listItem = this.closest('.list-item');
            if (listItem) {
                openEditListDialog(
                    listItem.dataset.listId,
                    listItem.dataset.listName,
                    listItem.dataset.listDescription,
                    listItem.dataset.listColor
                );
            }
        });

        // List delete buttons (sidebar)
        handleIconButtonClick('.delete-list-btn', function(e) {
            e.stopPropagation();
            const listItem = this.closest('.list-item');
            if (listItem) {
                confirmDeleteList(
                    listItem.dataset.listId,
                    listItem.dataset.listName
                );
            }
        });

        // List edit button (header)
        handleIconButtonClick('.edit-list-header-btn', function(e) {
            e.stopPropagation();
            const listContent = document.getElementById('list-content');
            if (listContent) {
                openEditListDialog(
                    listContent.dataset.listId,
                    listContent.dataset.listName,
                    listContent.dataset.listDescription,
                    listContent.dataset.listColor
                );
            }
        });

        // List delete button (header)
        handleIconButtonClick('.delete-list-header-btn', function(e) {
            e.stopPropagation();
            const listContent = document.getElementById('list-content');
            if (listContent) {
                confirmDeleteList(
                    listContent.dataset.listId,
                    listContent.dataset.listName
                );
            }
        });
    }

    // Initialize on page load
    initButtonHandlers();

    // Re-initialize after HTMX swaps
    document.body.addEventListener('htmx:afterSwap', () => {
        initButtonHandlers();
    });
});

// HTMX error handling
document.body.addEventListener('htmx:responseError', (evt) => {
    console.error('HTMX Error:', evt.detail);

    // Show error toast
    const alert = Object.assign(document.createElement('sl-alert'), {
        variant: 'danger',
        closable: true,
        duration: 5000,
        innerHTML: `
            <sl-icon slot="icon" name="exclamation-octagon"></sl-icon>
            An error occurred. Please try again.
        `
    });

    document.body.appendChild(alert);
    alert.toast();
});

// Handle HTMX after swap for list selection
document.body.addEventListener('htmx:afterSwap', (evt) => {
    // Update active list in sidebar after navigation
    if (evt.detail.target.id === 'main-content') {
        // Get list ID from URL
        const match = window.location.pathname.match(/\/app\/lists\/(.+)/);
        if (match) {
            const listId = match[1];
            // Remove active from all
            document.querySelectorAll('.list-item.active').forEach(el => {
                el.classList.remove('active');
            });
            // Add active to current
            const currentList = document.getElementById(`list-${listId}`);
            if (currentList) {
                currentList.classList.add('active');
            }
        }
    }
});

// Set no-cache headers for all responses
document.body.addEventListener('htmx:configRequest', (evt) => {
    evt.detail.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate';
    evt.detail.headers['Pragma'] = 'no-cache';
});
