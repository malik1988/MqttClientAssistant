#coding: utf-8
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, uic
import paho.mqtt.client as mqtt
from datetime import datetime

import os
uipath, uiname = os.path.split(os.path.realpath(__file__))
uiname = uiname.replace('.py', '.ui')
uifile = os.path.join(uipath, uiname)
ui_mainwindow, qtbaseclass = uic.loadUiType(uifile)


class MqttClientAssistant(ui_mainwindow, qtbaseclass):
    client = None
    is_connected = False
    topics = dict()  # 主题列表

    def __init__(self, parent=None):
        if not parent:
            parent = self
        ui_mainwindow.__init__(parent)
        qtbaseclass.__init__(parent)
        self.setupUi(parent)

        self.client = mqtt.Client()
        self.client.on_connect = self.mqtt_on_connected
        self.client.on_message = self.mqtt_on_message
        # 未连接服务器，禁用订阅
        self.pushButton_sub.setEnabled(False)

    def slot_connect_pressed(self):
        # 连接服务器点击事件
        if self.is_connected:  # 已经连接直接退出不处理
            return
        if self.lineEdit_server_port.text():
            port = int(self.lineEdit_server_port.text())
        else:
            port = 1883
        if self.lineEdit_user.text() and self.lineEdit_pwd.text():
            self.client.username_pw_set(self.lineEdit_user.text(),
                                        self.lineEdit_pwd.text())
        self.client.connect(self.lineEdit_server_ip.text(), port, 60)
        self.client.loop_start()

    def mqtt_on_connected(self, client, userdata, flags, rc):
        if rc == 0:
            print("Server Connected!")
            self.is_connected = True
            self.pushButton_sub.setEnabled(True)
            self.statusbar.showMessage("服务器连接成功！",msecs=5000)
        else:
            self.statusbar.showMessage("服务器连接失败！")
            print("Server Connect Failed, with result code " + str(rc))

    def mqtt_on_message(self, client, userdata, msg):
        text = '[%s] %r:%s ' % (
            datetime.now().strftime('%Y-%m-%d %H:%M:%S,%f'), msg.topic,
            bytes.decode(msg.payload))
        print(text)
        self.textBrowser.append(text)

    def slot_sub_pressed(self):
        # 订阅按键点击事件
        if not self.is_connected:
            QMessageBox.critical(self, "错误", "服务器未连接，请先连接服务器！")
            return

        if self.topics:
            # topics = [(topic, qos) for topic, qos in self.topics.items()]
            topics = []
            text = ""
            for topic, qos in self.topics.items():
                text += "%r" % topic + "," + str(qos) + "\n"
                topics.append((topic, qos))
            self.client.subscribe(topics)
            self.lineEdit_topic.setToolTip("已订阅主题：\n" + text)

    def slot_topic_change(self):
        # 主题文本修改事件(QOS变化事件也绑定到该函数)
        if self.lineEdit_topic.text() and self.lineEdit_qos.text():
            self.topics[self.lineEdit_topic.text()] = int(
                self.lineEdit_qos.text())

    def slot_msg_send(self):
        # 发布消息回车事件
        if not self.is_connected:
            QMessageBox.critical(self, "错误", "服务器未连接，请先连接服务器！")
            return

        topic = self.lineEdit_topic.text()
        msg = self.lineEdit_msg_pub.text()
        qos = self.lineEdit_qos.text()
        if topic and msg and qos:
            qos = int(qos)
            self.client.publish(topic, msg, qos)
