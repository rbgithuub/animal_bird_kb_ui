const form = document.getElementById("animal-form");
const tableBody = document.querySelector("#animals-table tbody");

const API_URL = "http://localhost:5000";

// Fetch and display all animals
//async function loadAnimals() {
//  const res = await fetch(`${API_URL}/animals`);
//  const data = await res.json();
// tableBody.innerHTML = "";
//  data.forEach((animal) => {
//    const row = document.createElement("tr");
//    row.innerHTML = `
//      <td>${animal.name}</td>
//      <td>${animal.category}</td>
//     <td>${animal.origin}</td>
//      <td>${animal.sleep_pattern}</td>
//      <td>${animal.food_habits}</td>
//      <td><ul>${animal.fun_facts.map(f => `<li>${f}</li>`).join("")}</ul></td>
//      <td>
//        <button class="btn btn-warning btn-sm" onclick="editAnimal('${animal._id}')">Edit</button>
//        <button class="btn btn-danger btn-sm" onclick="deleteAnimal('${animal._id}')">Delete</button>
//      </td>
//    `;
//    tableBody.appendChild(row);
//  });
//}
async function loadAnimals() {
  const res = await fetch('/animals');
  const animals = await res.json();

  const tableBody = document.getElementById('animalTableBody');
  tableBody.innerHTML = ''; // Clear old rows

  animals.forEach(animal => {
      const row = `<tr>
          <td>${animal.name}</td>
          <td>${animal.category}</td>
          <td>${animal.origin}</td>
          <td>${animal.sleep_pattern}</td>
          <td>${animal.food_habits}</td>
          <td>${animal.fun_facts.join(', ')}</td>
          <td>
              <button class="btn btn-sm btn-warning" onclick="editAnimal('${animal._id}')">Edit</button>
              <button class="btn btn-sm btn-danger" onclick="deleteAnimal('${animal._id}')">Delete</button>
          </td>
      </tr>`;
      tableBody.innerHTML += row;
  });
}


// Handle form submission
form.addEventListener("submit", async (e) => {
  e.preventDefault();
  const newAnimal = {
    name: form.name.value,
    category: form.category.value,
    origin: form.origin.value,
    sleep_pattern: form.sleep_pattern.value,
    food_habits: form.food_habits.value,
    fun_facts: form.fun_facts.value.split(",").map(f => f.trim())
  };
  await fetch(`${API_URL}/animals`, {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify([newAnimal])  // using bulk insert
  });
  form.reset();
  loadAnimals();
});

// Delete an animal
async function deleteAnimal(id) {
  await fetch(`${API_URL}/animals/${id}`, { method: "DELETE" });
  loadAnimals();
}

// Edit (update) an animal
//async function editAnimal(id) {
 // const res = await fetch(`${API_URL}/animals`);
  //const data = await res.json();
 // const animal = data.find(a => a._id === id);

//  form.name.value = animal.name;
//  form.category.value = animal.category;
//  form.origin.value = animal.origin;
//  form.sleep_pattern.value = animal.sleep_pattern;
//  form.food_habits.value = animal.food_habits;
// form.fun_facts.value = animal.fun_facts.join(", ");
async function submitEdit(event) {
  event.preventDefault();

  const id = document.getElementById('edit_id').value;

  const data = {
      name: document.getElementById('edit_name').value,
      category: document.getElementById('edit_category').value,
      origin: document.getElementById('edit_origin').value,
      sleep_pattern: document.getElementById('edit_sleep_pattern').value,
      food_habits: document.getElementById('edit_food_habits').value,
      fun_facts: document.getElementById('edit_fun_facts').value.split(';').map(f => f.trim())
  };

  const response = await fetch(`/animals/${id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
  });

  if (response.ok) {
      const modal = bootstrap.Modal.getInstance(document.getElementById('editModal'));
      modal.hide();
      loadAnimals(); // Refresh data
  } else {
      alert('Failed to update animal. Check console for details.');
      console.error(await response.text());
  }
}


  // Modify form submission for update
  form.onsubmit = async (e) => {
    e.preventDefault();
    const updatedAnimal = {
      name: form.name.value,
      category: form.category.value,
      origin: form.origin.value,
      sleep_pattern: form.sleep_pattern.value,
      food_habits: form.food_habits.value,
      fun_facts: form.fun_facts.value.split(",").map(f => f.trim())
    };
    await fetch(`${API_URL}/animals/${id}`, {
      method: "PUT",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify(updatedAnimal)
    });
    form.reset();
    form.onsubmit = null;  // Reset to default behavior
    form.addEventListener("submit", e => e.preventDefault());
    loadAnimals();
  };
}

loadAnimals();
