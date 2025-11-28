const tasks = [];
let idCounter = 1;

const form = document.getElementById('task-form');
const bulkInput = document.getElementById('bulk_input');
const analyzeBtn = document.getElementById('analyze-btn');
const output = document.getElementById('output');
const feedback = document.getElementById('feedback');
const strategySelect = document.getElementById('strategy');

// Handle add-task form submission
form.addEventListener('submit', (e) => {
  e.preventDefault();
  feedback.textContent = '';

  const title = document.getElementById('title').value.trim();
  const due_date = document.getElementById('due_date').value;
  const estimated_hours = parseFloat(document.getElementById('estimated_hours').value);
  const importance = parseInt(document.getElementById('importance').value);
  const depsRaw = document.getElementById('dependencies').value;

  if (!title || !due_date || isNaN(estimated_hours) || isNaN(importance)) {
    feedback.textContent = 'Please fill all required fields correctly.';
    return;
  }

  const dependencies = depsRaw
    .split(',')
    .map((x) => x.trim())
    .filter((x) => x !== '')
    .map((x) => parseInt(x));

  const task = {
    id: idCounter++,
    title,
    due_date,
    estimated_hours,
    importance,
    dependencies,
  };

  tasks.push(task);

  form.reset();
  feedback.textContent = `Task added (total: ${tasks.length}). Click "Analyze Tasks" to see priority.`;
});

// Handle Analyze button click
analyzeBtn.addEventListener('click', async () => {
  feedback.textContent = '';

  let payloadTasks = tasks;

  // If bulk JSON is provided, use that instead of in-memory tasks
  if (bulkInput.value.trim()) {
    try {
      payloadTasks = JSON.parse(bulkInput.value);
      if (!Array.isArray(payloadTasks)) {
        throw new Error('Bulk input must be a JSON array.');
      }
    } catch (e) {
      feedback.textContent = 'Invalid JSON in bulk input.';
      output.innerHTML = '';
      return;
    }
  }

  if (!payloadTasks.length) {
    feedback.textContent = 'Add at least one task (form or bulk JSON).';
    output.innerHTML = '';
    return;
  }

  const strategy = strategySelect ? strategySelect.value : '';

  if (!strategy) {
    feedback.textContent = 'Please select a sorting strategy.';
    output.innerHTML = '';
    return;
  }

  output.innerHTML = 'Analyzing...';

  try {
    console.log('USING STRATEGY:', strategy, 'TASKS:', payloadTasks);
    const res = await fetch('/api/tasks/analyze/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        tasks: payloadTasks,
        strategy: strategy,
      }),
    });

    if (!res.ok) {
      throw new Error('Server error ' + res.status);
    }

    const analyzed = await res.json();
    renderTasks(analyzed, strategy);
  } catch (err) {
    console.error(err);
    feedback.textContent = 'Failed to analyze tasks: ' + err.message;
    output.innerHTML = '';
  }
});

// Render analyzed & sorted tasks
function renderTasks(list, strategy) {
  if (!Array.isArray(list) || !list.length) {
    output.innerHTML = '<p>No tasks.</p>';
    return;
  }

  output.innerHTML = '';

  const heading = document.createElement('p');
  heading.textContent = `Showing ${list.length} tasks using strategy: ${labelForStrategy(
    strategy
  )}`;
  output.appendChild(heading);

  list.forEach((task) => {
    const score = typeof task.score === 'number' ? task.score : null;

    let level = 'low';
    if (score !== null) {
      if (score >= 7) level = 'high';
      else if (score >= 4) level = 'medium';
    }

    const div = document.createElement('div');
    div.className = `task-card ${level}`;

    const deps = Array.isArray(task.dependencies) ? task.dependencies.join(', ') : '';

    div.innerHTML = `
      <strong>${escapeHtml(task.title || '')}</strong>
      ${score !== null ? `(Score: ${score.toFixed(2)})` : ''}<br>
      Due: ${task.due_date || 'N/A'} |
      Effort: ${task.estimated_hours ?? 'N/A'} h |
      Importance: ${task.importance ?? 'N/A'}<br>
      Dependencies: ${deps || 'None'}
    `;

    output.appendChild(div);
  });
}

function labelForStrategy(value) {
  switch (value) {
    case 'fastest':
      return 'Fastest Wins';
    case 'impact':
      return 'High Impact';
    case 'deadline':
      return 'Deadline Driven';
    case 'smart':
    default:
      return 'Smart Balance';
  }
}

// Simple HTML escape to avoid XSS in titles
function escapeHtml(str) {
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;');
}

