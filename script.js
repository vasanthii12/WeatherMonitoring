document.addEventListener('DOMContentLoaded', function() {
  fetchWeatherData();
  setupCitySelect();
  window.weatherInterval = setInterval(fetchWeatherData, getUpdateInterval() * 60000);
});

function setupEventListeners() {
  document.getElementById('tempUnit').addEventListener('change', updateTemperatureUnit);
  document.getElementById('updateInterval').addEventListener('change', updateInterval);
  document.getElementById('alertThreshold').addEventListener('change', updateAlertThreshold);
}

function updateTemperatureUnit() {
  fetchWeatherData(); 
}

function updateInterval() {
  clearInterval(window.weatherInterval);
  window.weatherInterval = setInterval(fetchWeatherData, getUpdateInterval() * 60000);
  console.log(`Update interval set to ${getUpdateInterval()} minutes`);
}

function updateAlertThreshold() {
  console.log(`Alert threshold set to ${getAlertThreshold()}°${getTemperatureUnit()}`);
  fetchWeatherData();
}

function getUpdateInterval() {
  return parseInt(document.getElementById('updateInterval').value) || 5;
}

function getAlertThreshold() {
  return parseFloat(document.getElementById('alertThreshold').value) || 30;
}

function getTemperatureUnit() {
  return document.getElementById('tempUnit').checked ? 'F' : 'C';
}

function convertTemperature(temp, toFahrenheit) {
  return toFahrenheit ? (temp * 9/5) + 32 : temp;
}

function fetchWeatherData() {
  fetch('/api/weather')
      .then(response => response.json())
      .then(data => {
          const isFahrenheit = document.getElementById('tempUnit').checked;
          const convertedData = data.map(city => ({
              ...city,
              temp: convertTemperature(city.temp, isFahrenheit),
              feels_like: convertTemperature(city.feels_like, isFahrenheit)
          }));
          updateCityOverview(convertedData, isFahrenheit);
          populateCitySelect(convertedData);
          createWeatherChart(convertedData, isFahrenheit);
          checkAlerts(convertedData);
      })
      .catch(error => console.error('Error:', error));
}

function updateCityOverview(data, isFahrenheit) {
  const overviewContainer = document.getElementById('city-overview');
  overviewContainer.innerHTML = '';
  
  data.forEach(city => {
      const cityElement = document.createElement('div');
      cityElement.className = 'city-card';
      cityElement.innerHTML = `
          <h3>${city.name}</h3>
          <i class="${getWeatherIcon(city.main)} weather-icon"></i>
          <p><i class="fas fa-thermometer-half"></i> ${city.temp.toFixed(1)}°${isFahrenheit ? 'F' : 'C'}</p>
          <p>${city.main}</p>
      `;
      overviewContainer.appendChild(cityElement);
  });
}

function checkAlerts(data) {
  const threshold = getAlertThreshold();
  const alertsList = document.getElementById('alertsList');
  alertsList.innerHTML = '';

  data.forEach(city => {
      if (city.temp > threshold) {
          const alertItem = document.createElement('div');
          alertItem.className = 'alert-item';
          alertItem.innerHTML = `
                <i class="fas fa-exclamation-circle"></i>
                High temperature alert in ${city.name}: ${city.temp.toFixed(1)}°${getTemperatureUnit()}
                <br>
                <small>${new Date().toLocaleString()}</small>
            `;
            alertsList.appendChild(alertItem);
        }
    });
}

function updateCityDetails(data, isFahrenheit) {
  const detailsContainer = document.getElementById('city-details');
  detailsContainer.innerHTML = `
      <h3>${data.name}</h3>
      <i class="${getWeatherIcon(data.main)} weather-icon large"></i>
      <p><i class="fas fa-thermometer-half"></i> Temperature: ${data.temp.toFixed(1)}°${isFahrenheit ? 'F' : 'C'}</p>
      <p><i class="fas fa-thermometer"></i> Feels Like: ${data.feels_like.toFixed(1)}°${isFahrenheit ? 'F' : 'C'}</p>
      <p><i class="fas fa-tint"></i> Humidity: ${data.humidity}%</p>
      <p><i class="fas fa-wind"></i> Wind Speed: ${data.wind_speed} m/s</p>
      <p><i class="${getWeatherIcon(data.main)}"></i> Weather: ${data.main}</p>
  `;
}

function createWeatherChart(data, isFahrenheit) {
  const ctx = document.getElementById('weatherChart').getContext('2d');
  
  const labels = data.map(city => city.name);
  const temperatures = data.map(city => city.temp);
  const humidities = data.map(city => city.humidity);

  new Chart(ctx, {
      type: 'bar',
      data: {
          labels: labels,
          datasets: [
              {
                  label: `Temperature (°${isFahrenheit ? 'F' : 'C'})`,
                  data: temperatures,
                  backgroundColor: 'rgba(255, 99, 132, 0.6)',
                  borderColor: 'rgba(255, 99, 132, 1)',
                  borderWidth: 1
              },
              {
                  label: 'Humidity (%)',
                  data: humidities,
                  backgroundColor: 'rgba(138, 43, 226, 0.6)',
                  borderColor: 'rgba(138, 43, 226, 1)',
                  borderWidth: 1
              }
          ]
      },
      options: {
          responsive: true,
          plugins: {
              title: {
                  display: true,
                  text: 'Temperature and Humidity Comparison Across Cities',
                  color: '#333',
                    font: {
                        size: 16,
                        weight: 'bold'
                    }
                },
                legend: {
                    labels: {
                        color: '#333'
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Value',
                        color: '#333'
                    },
                    ticks: {
                        color: '#333'
                    }
                },
                x: {
                    ticks: {
                        color: '#333'
                    }
                }
            }
        }
    });
}
function fetchWeatherData() {
  fetch('/api/weather')
      .then(response => response.json())
      .then(data => {
          updateCityOverview(data);
          populateCitySelect(data);
          createWeatherChart(data); 
      })
      .catch(error => console.error('Error:', error));
}

  const weatherIcons = {
    'Clear': 'fas fa-sun',
    'Clouds': 'fas fa-cloud',
    'Rain': 'fas fa-cloud-rain',
    'Drizzle': 'fas fa-cloud-rain',
    'Thunderstorm': 'fas fa-bolt',
    'Snow': 'fas fa-snowflake',
    'Mist': 'fas fa-smog',
    'Smoke': 'fas fa-smog',
    'Haze': 'fas fa-smog',
    'Dust': 'fas fa-smog',
    'Fog': 'fas fa-smog',
    'Sand': 'fas fa-wind',
    'Ash': 'fas fa-smog',
    'Squall': 'fas fa-wind',
    'Tornado': 'fas fa-wind'
};

function getWeatherIcon(condition) {
  return weatherIcons[condition] || 'fas fa-question';
}

function updateCityOverview(data) {
  const overviewContainer = document.getElementById('city-overview');
  overviewContainer.innerHTML = '';
  
  data.forEach(city => {
      const cityElement = document.createElement('div');
      cityElement.className = 'city-card';
      cityElement.innerHTML = `
          <h3>${city.name}</h3>
          <i class="${getWeatherIcon(city.main)} weather-icon"></i>
          <p><i class="fas fa-thermometer-half"></i> ${city.temp.toFixed(1)}°C</p>
          <p>${city.main}</p>
      `;
      overviewContainer.appendChild(cityElement);
  });
}

function updateCityDetails(data) {
  const detailsContainer = document.getElementById('city-details');
  detailsContainer.innerHTML = `
      <h3>${data.name}</h3>
      <i class="${getWeatherIcon(data.main)} weather-icon large"></i>
      <p><i class="fas fa-thermometer-half"></i> Temperature: ${data.temp.toFixed(1)}°C</p>
      <p><i class="fas fa-thermometer"></i> Feels Like: ${data.feels_like.toFixed(1)}°C</p>
      <p><i class="fas fa-tint"></i> Humidity: ${data.humidity}%</p>
      <p><i class="fas fa-wind"></i> Wind Speed: ${data.wind_speed} m/s</p>
      <p><i class="${getWeatherIcon(data.main)}"></i> Weather: ${data.main}</p>
  `;
}

function setupCitySelect() {
  const citySelect = document.getElementById('city-select');
  citySelect.addEventListener('change', function() {
      const selectedCity = this.value;
      if (selectedCity) {
          fetchCityDetails(selectedCity);
      } else {
          document.getElementById('city-details').innerHTML = '';
      }
  });
}

function populateCitySelect(data) {
  const citySelect = document.getElementById('city-select');
  data.forEach(city => {
      const option = document.createElement('option');
      option.value = city.name;
      option.textContent = city.name;
      citySelect.appendChild(option);
  });
}

function fetchCityDetails(city) {
  fetch(`/api/weather/${city}`)
      .then(response => response.json())
      .then(data => {
          updateCityDetails(data);
      })
      .catch(error => console.error('Error:', error));
}

function updateCityDetails(data) {
  const detailsContainer = document.getElementById('city-details');
  detailsContainer.innerHTML = `
      <h3>${data.name}</h3>
      <p>Temperature: ${data.temp.toFixed(1)}°C</p>
      <p>Feels Like: ${data.feels_like.toFixed(1)}°C</p>
      <p>Humidity: ${data.humidity}%</p>
      <p>Wind Speed: ${data.wind_speed} m/s</p>
      <p>Weather: ${data.main}</p>
  `;
}

function checkAlerts(data, isFahrenheit) {
  const threshold = parseFloat(document.getElementById('alertThreshold').value);
  const alertsList = document.getElementById('alertsList');
  alertsList.innerHTML = '';

  data.forEach(city => {
      if (city.temp > threshold) {
          const alertItem = document.createElement('div');
          alertItem.className = 'alert-item';
          alertItem.innerHTML = `
              <i class="fas fa-exclamation-circle"></i>
              High temperature alert in ${city.name}: ${city.temp.toFixed(1)}°${isFahrenheit ? 'F' : 'C'}
              <br>
              <small>${new Date().toLocaleString()}</small>
          `;
          alertsList.appendChild(alertItem);
      }
  });
}