const tasks = [];
let idCounter = 1;

const form = document.getElementById('task-form');
const bulkInput = document.getElementById('bulk_input');
const analyzeBtn = document.getElementById('analyze-btn');
const output = document.getElementById('output');
const feedback = document.getElementById('feedback');

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
    .map(x => x.trim())
    .filter(x => x !== '')
    .map(x => parseInt(x));

  tasks.push({
    id: idCounter++,
    title,
    due_date,
    estimated_hours,
    importance,
    dependencies
  });

  form.reset();
  feedback.textContent = 'Task added. Click "Analyze Tasks" to see priority.';
});

analyzeBtn.addEventListener('click', async () => {
  feedback.textContent = '';
  let payloadTasks = tasks;

  if (bulkInput.value.trim()) {
    try {
      payloadTasks = JSON.parse(bulkInput.value);
    } catch (e) {
      feedback.textContent = 'Invalid JSON in bulk input.';
      return;
    }
  }

  if (!payloadTasks.length) {
    feedback.textContent = 'Add at least one task.';
    return;
  }

  output.innerHTML = 'Analyzing...';

  try {
    const res = await fetch('/api/tasks/analyze/', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({tasks: payloadTasks})
    });

    if (!res.ok) {
      throw new Error('Server error ' + res.status);
    }

    const analyzed = await res.json();
    renderTasks(analyzed);
  } catch (err) {
    feedback.textContent = err.message;
    output.innerHTML = '';
  }
});

function renderTasks(list) {
  if (!list.length) {
    output.innerHTML = '<p>No tasks.</p>';
    return;
  }
  output.innerHTML = '';
  list.forEach(task => {
    let level = 'low';
    if (task.score >= 7) level = 'high';
    else if (task.score >= 4) level = 'medium';

    const div = document.createElement('div');
    div.className = level;
    div.innerHTML = `
      <strong>${task.title}</strong> (Score: ${task.score})<br>
      Due: ${task.due_date} | Effort: ${task.estimated_hours}h | Importance: ${task.importance}
    `;
    output.appendChild(div);
  });
}
