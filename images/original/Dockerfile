FROM node:11


RUN date >build_date.txt
RUN npm install serialport
RUN npm install https://github.com/haakonklausen/mbusparser --save
RUN git clone https://github.com/haakonklausen/mbusreader
RUN cd mbusreader
RUN npm install

CMD node mbusreader/mbusreader.js
