// // note that the chart container has `ondragover` and `ondrop` event handlers registered
// // and the draggable items have `onselectstart`, `ondragstart` and `ondragend`.
//
// /** The node on which the mouse cursor is currently hovering. */
// var currentHoverNode = null;
// var draggedColor = null;
// var nodeColorMap = {};
//
// function colorSelectStart(event, elem) {
//     // workaround to enable drag-n-drop in IE9: http://stackoverflow.com/q/5500615/1711598
//     if (elem.dragDrop) {
//         elem.dragDrop();
//     }
//
//     return false;
// }
//
// function colorDragStart(event, elem) {
//     // cannot use `event.dataTransfer.setData`: http://stackoverflow.com/a/11959389/1711598
//     draggedColor = elem.style.backgroundColor;
//
//     // but it is needed for Firefox otherwise draggin does not start.
//     event.dataTransfer.setData("text", draggedColor);
// }
//
// function colorDragEnd(event) {
//     draggedColor = null;
// }
//
// function networkDragOver(event) {
//     if (draggedColor && currentHoverNode) {
//         // this instructs the browser to allow the drop
//         event.preventDefault();
//     }
// }
//
// function networkDragDrop(event) {
//     if (draggedColor && currentHoverNode) {
//         nodeColorMap[currentHoverNode.id] = draggedColor;
//         t.updateStyle();
//     }
//
//     event.preventDefault();
// }
//
// function networkHoverChanged(event) {
//     currentHoverNode = event.hoverNode;
// }
//
// function networkNodeStyleFunction(node) {
//     var color = nodeColorMap[node.id];
//     if (color)
//         node.fillColor = color;
// }
//
// function buildData() {
//
// }
//
//
// document.addEventListener("DOMContentLoaded", function () {
//     var t = new NetChart({
//         container: "demo",
//         area: {height: window.screen.height - 150},
//         data: {url: "http://127.0.0.1:5000/get_nodes_n_links"},
//         nodeMenu: {enabled: false},
//         linkMenu: {enabled: false},
//         style: {
//             nodeAutoScaling: "linear",
//             nodeDetailMinSize: 0
//         },
//         layout: {
//             nodeSpacing: 20
//         },
//         navigation: {
//             mode: "showall"
//         },
//
//         theme: NetChart.themes.dark,
//
//         interaction: {
//             resizing: {enabled: false},
//             zooming: {
//                 zoomExtent: [0.1, 2],
//                 autoZoomExtent: [0.1, 1]
//             }
//         }
//
//     });
// });

document.addEventListener("DOMContentLoaded", function () {
    var randomSeed = 10; // this can be changed to generate different data sets
    var nextNodeId = 0;
    var iter = 80;
    var chart = null;

    function buildData(nodeList, success, fail) {
        // build a random graph
        var links = [];
        var nodes = [];

        fetch('http://127.0.0.1:5000/get_nodes_n_links')
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json(); // Parse the response body as JSON
            })
            .then(data => {
                nodes = data.nodes;
                links = data.links;


                success({"nodes": nodes, "links": links}); // Call success function with data
            })
            .catch(error => {
                console.error('Error:', error); // Handle any errors that occur during the request
                fail(); // Call fail function on error
            });
    }

    function linkStyle(link) {
        link.length = 1;
        link.radius = 1;
        link.fromDecoration = "circle";
        link.toDecoration = "hollow arrow";

        link.fillColor = "#FFFFFF";

        var trafficWeight = link.data.traffic; // Assuming 'traffic' is a measure of traffic intensity

        var link_color = "#FFFFFF"

        // Change color based on traffic intensity (this is just an example)
        if (trafficWeight > 5) {

            link.lineDash = 20;

            link.fillColor = "#FF0000"; // High traffic in red
            link.radius = 3;

        } else {
            link.fillColor = "#FFFFFF"; // Lower traffic in green
        }


        link.items = [
            {   // Default item places just as the regular label.
                text: link.data.weight,
                padding: 2,
                backgroundStyle: {
                    // fillColor: "rgba(0,0,0, 1)",
                    fillColor: "rgba(0,0,0, 1)",
                },
                textStyle: {
                    fillColor: "white",
                    font: "15px FontAwesome"

                }
            },
        ]
    }

    chart = new NetChart({
        container: document.getElementById("demo"),
        data: {dataFunction: buildData},
        area: {height: window.screen.height - 250},

        nodeMenu: {enabled: false},
        linkMenu: {enabled: false},

        style: {
            node: {
                display: "roundtext",
            },
            nodeLabel: {
                align: "center",
                textStyle: {
                    fillColor: "#000000",
                    font: "15px FontAwesome"
                }
            },

            nodeAutoScaling: "linear",
            nodeDetailMinSize: 0,
            linkStyleFunction: linkStyle,
        },

        credis: {
            image: ""
        },

        layout: {
            // mode: "hierarchy",
            nodeSpacing: 200,
            gravity: {
                from: "auto",
                to: "nearestLockedNode",
                strength: 0.001,
            },
        },
        navigation: {
            mode: "showall"
        },

        theme: NetChart.themes.dark,
        legend: {enabled: true},

        title: {
            text: "Data (traffic) Architecture Simulator"
        },

        toolbar: {},

        selection: {

        },

        interaction: {
            resizing: {enabled: true},
            nodeMenu: {showData: true},
            selection: {linksSelectable: false},
            rotation: {fingers: true},
            zooming: {
                zoomExtent: [0.1, 9],
                autoZoomExtent: [0.1, 1]
            }
        }
    });

    // Reload data every 5 seconds (5000 milliseconds)
    var intervalHandle = setInterval(function () {
        chart.reloadData();
    }, 500);

    function disposeDemo() {
        clearInterval(intervalHandle); // Clear the interval
        disposeDemo = null; // Clear the disposeDemo function
        intervalHandle = null; // Clear the interval handle
    }
});





