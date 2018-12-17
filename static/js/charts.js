function score_chart(container_id, title, x_data, y_data) {
  let dom = document.getElementById(container_id);
  let myChart = echarts.init(dom);
  let app = {};
  option = null;
  let data = [
    ['compoundA', 50], ['compoundE', 30], ['compoundC', 30], ['compoundD', 10], ['compoundB', 200]
  ];

  option = {
    title: {
      text: title,
      // subtext: 'By ',
      sublink: 'https://github.com/ecomfe/echarts-stat',
      left: 'left',
      top: 0,
      textStyle: {
        color: '#ffffff',
        fontSize: '26',
      }
    },
    xAxis: {
      type: 'category',
      data: x_data,
      axisLine: {
        lineStyle: {
          color: '#87889c'
        }
      },
    },
    yAxis: {
      type: 'value',
      axisLine: {
        lineStyle: {
          color: '#87889c'
        }
      },
    },
    series: [{
      data: y_data,
      type: 'line',
      smooth: true,
      itemStyle: {
        color: '#4297c3'
      }
    }]
  };
  ;
  if (option && typeof option === "object") {
    myChart.setOption(option, true);
  }
}

