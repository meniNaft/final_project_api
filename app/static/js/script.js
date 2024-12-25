document.addEventListener('DOMContentLoaded', () => {
  const endpointSelect = document.getElementById('endpoint');
  const paramsContainer = document.getElementById('params-container');
  const submitButton = document.getElementById('submit');
  const resultContainer = document.getElementById('json-output');
  const mapContainer = document.getElementById('map-container');  // New container for map

  const endpoints = [
    { name: 'Deadliest Attack Types', value: 'statistics/deadliest-attack-types', params: ['filter_top5'] },
    { name: 'Avg Casualties Per Area', value: 'statistics/avg-casualties-per-area', params: ['area_type', 'filter_top5'] },
    { name: 'Top Terror Groups By Casualties', value: 'statistics/top-terror-groups-by-casualties', params: [] },
    { name: 'Attack Percentage Change By Year', value: 'statistics/attack-percentage-change-by-year', params: ['area_type', 'area_id'] },
    { name: 'Most Active Terror Group', value: 'statistics/most-active-terror-group', params: ['area_type', 'area_id'] },

    { name: 'Terror Groups With Shared Targets By Area', value: 'statistics/relationship/shared-targets', params: ['area_type'] },
    { name: 'Cooperating Terror Groups', value: 'statistics/relationship/cooperating-groups', params: [] },
    { name: 'Terror Groups With Shared Attack Types By Area', value: 'statistics/relationship/shared-attack-types', params: ['area_type'] },
    { name: 'Top Group City By Area', value: 'statistics/relationship/top-group-city', params: ['area_type'] },
    { name: 'Groups Attacked Same Target Same Year', value: 'statistics/relationship/groups-attacked-same-target-same-year', params: [] },

    { name: 'Search Keywords', value: 'search/keywords', params: ['query'] },
    { name: 'Search News', value: 'search/news', params: ['query'] },
    { name: 'Search Historic', value: 'search/historic', params: ['query'] },
    { name: 'Search Combined', value: 'search/combined', params: ['query', 'start_date', 'end_date'] }
  ];

  // Populate dropdown options
  endpoints.forEach(endpoint => {
    const option = document.createElement('option');
    option.value = endpoint.value;
    option.textContent = endpoint.name;
    endpointSelect.appendChild(option);
  });

  // Handle parameter fields based on endpoint selection
  endpointSelect.addEventListener('change', () => {
    paramsContainer.innerHTML = '';
    const selectedEndpoint = endpoints.find(e => e.value === endpointSelect.value);

    if (selectedEndpoint) {
      selectedEndpoint.params.forEach(param => {
        const label = document.createElement('label');
        label.textContent = `Enter ${param}:`;

        const input = document.createElement('input');
        input.type = 'text';
        input.id = param;

        paramsContainer.appendChild(label);
        paramsContainer.appendChild(input);
      });

      const searchEndpoints = [
      'search/keywords',
      'search/news',
      'search/historic',
      'search/combined'
    ];

    if (searchEndpoints.includes(selectedEndpoint.value)) {
      const label = document.createElement('label');
      label.textContent = "Enter limit (optional):";

      const input = document.createElement('input');
      input.type = 'text';
      input.id = 'limit';  // Add input for limit

      paramsContainer.appendChild(label);
      paramsContainer.appendChild(input);
    }
    }
  });

  // Submit request
  submitButton.addEventListener('click', async () => {
    const selectedEndpoint = endpoints.find(e => e.value === endpointSelect.value);
    if (!selectedEndpoint) {
      resultContainer.textContent = 'Please select an endpoint.';
      return;
    }

    let url = `/api/${selectedEndpoint.value}`;
    const queryParams = selectedEndpoint.params.map(param => {
      const input = document.getElementById(param);
      return input ? input.value : '';
    }).join('/');

    if (queryParams) {
      url += `/${queryParams}`;
    }

    const limit = document.getElementById('limit') ? document.getElementById('limit').value : '';
    if (limit) {
      url += `?limit=${limit}`;
    }

    try {
      const response = await fetch(url);
      const contentType = response.headers.get('Content-Type');

      // Clear the previous results
      resultContainer.textContent = '';

      mapContainer.innerHTML = '';  // Clear map container

      if (contentType.includes('html')) {
        // If it's a map (HTML), display it
        const mapHtml = await response.text();
        mapContainer.innerHTML = mapHtml;  // Insert the map HTML into the container
      } else if (contentType.includes('json')) {
        // If it's JSON, display it as formatted text
        const data = await response.json();
        resultContainer.textContent = JSON.stringify(data, null, 2);
      } else {
        resultContainer.textContent = 'Unknown response type.';
      }
    } catch (error) {
      resultContainer.textContent = 'Error fetching data.';
    }
  });
});
