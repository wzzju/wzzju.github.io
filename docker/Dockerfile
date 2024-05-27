FROM jekyll/jekyll:latest

ENV TZ=Asia/Shanghai
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN gem install github-pages
RUN gem install jekyll
RUN gem install jekyll-redirect-from
RUN gem install kramdown
RUN gem install rdiscount
RUN gem install rouge

VOLUME /src
EXPOSE 4000

WORKDIR /src
