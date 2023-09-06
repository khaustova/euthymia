let url = "https://api-metrika.yandex.net/stat/v1/data/bytime?metrics=ym:s:hits,ym:s:users&date1=6daysAgo&date2=today&group=day&filters=ym:s:isRobot=='No'&id=94751613";

async function getJSONData() {
  const response = await fetch(url)
  const json = await response.json();
  return json
}

getJSONData().then(data => {
  data;
  chartMetrics(data['totals'][0], 'viewChart');
  chartMetrics(data['totals'][1], 'guestChart');
});

async function chartMetrics(data, chartId) {
  new Chart(
    document.getElementById(chartId),
    {
      type: 'line',
      options: {
        plugins: {
          legend: {
            display: false,
          },
        },
        scales: {
          x: {
            display: false,
          },
          y: {
            display: false,
          }
        }
      },
      data: {
        labels: ['6 дней назад', '5 дней назад', '4 дня назад', '3 дня назад', '2 дня назад', 'вчера', 'сегодня'],
        datasets: [
          {
            data: data,
            backgroundColor: '#00a194',
            borderColor: '#00a194',
          }
        ],
      }
    }
  );
};

