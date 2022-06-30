import QtQuick
import QtQuick.Controls.Basic
import QtQuick.Layouts

ApplicationWindow {
    visible: true
    width: 800
    height: 600
    x: screen.desktopAvailableWidth - width - 12
    y: screen.desktopAvailableHeight - height - 48
    title: "Nature News"

    // flags: Qt.FramelessWindowHint | Qt.Window

    property string currTime: "00:00:00"
    property int min: 100
    property int curr_min: 250

    property int curr_max: 600
    property int max: 800
    property QtObject backend

    ColumnLayout {
        anchors.fill: parent
        spacing: 20
        Image {
            sourceSize.width: parent.width
            sourceSize.height: parent.height
            source: "./images/bkgnd.jpg"
            fillMode: Image.PreserveAspectFit
        }
        TextField {
            id: test
            placeholderText: qsTr("Test")
            width: 70
            Layout.alignment: Qt.AlignHCenter
            font.pointSize: 14
            selectByMouse: true
        }
        Button {
            text: "Generate Weekly News Summaries"
            width: 100
            Layout.alignment: Qt.AlignHCenter
            onClicked: {
                backend.getNews(config_slider.value)
                result_lbl.text = "Gathering Life Cycle Assessment News"
            }
        }
        Label {
            width: 100
            Layout.alignment: Qt.AlignHCenter
            id: result_lbl
        }
        Slider {
            id: config_slider
            from: min
            value: curr_min
            to: max
            Layout.alignment: Qt.AlignHCenter
        }
        Text {
            anchors {
                bottom: parent.bottom
                bottomMargin: 12
                left: parent.left
                leftMargin: 12
            }
            text: currTime
            font.pixelSize: 48
            color: "white"
        }
    }

    Connections {
        target: backend

        function onUpdated(msg) {
            currTime = msg;
        }
    }
}