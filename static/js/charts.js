function score_chart(container_id) {
  let dom = document.getElementById(container_id);
  let myChart = echarts.init(dom);
  let app = {};
  option = null;
  let data = [
    ['compoundA', 50], ['compoundE', 30], ['compoundC', 30], ['compoundD', 10], ['compoundB', 200]
  ];

  // See https://github.com/ecomfe/echarts-stat
  let myRegression = ecStat.regression('exponential', data);

  myRegression.points.sort(function (a, b) {
    return a[0] - b[0];
  });

  option = {
    title: {
      text: 'score',
      // subtext: 'By ',
      sublink: 'https://github.com/ecomfe/echarts-stat',
      left: 'center'
    },
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'cross'
      }
    },
    xAxis: {
      name: 'compound',
      type: 'category',
      data: ['compoundA', 'compoundB', 'compoundC', 'compoundD', 'compoundE', 'compoundF', 'compoundG'],
      splitLine: {
        lineStyle: {
          type: 'dashed'
        }
      },
    },
    yAxis: {
      name: 'score',
      type: 'value',
      splitLine: {
        lineStyle: {
          type: 'dashed'
        }
      }
    },
    series: [{
      name: 'scatter',
      type: 'scatter',
      label: {
        emphasis: {
          show: true,
          position: 'left',
          textStyle: {
            color: 'blue',
            fontSize: 16
          }
        }
      },
      data: data
    }, {
      name: 'line',
      type: 'line',
      showSymbol: false,
      smooth: true,
      data: data,
      markPoint: {
        itemStyle: {
          normal: {
            color: 'transparent'
          }
        },
        label: {
          normal: {
            show: true,
            position: 'left',
            formatter: myRegression.expression,
            textStyle: {
              color: '#333',
              fontSize: 14
            }
          }
        },
        data: [{
          coord: myRegression.points[myRegression.points.length - 1]
        }]
      }
    }]
  };
  ;
  if (option && typeof option === "object") {
    myChart.setOption(option, true);
  }
}