# 开发文档

## 提供接口

### 版本

`/api/acfun-helper/options/upload`

请求方式:`GET`

返回版本号，其他接口请求数据格式或返回格式变更后会修改版本号

### 上传

接口:`/api/acfun-helper/options/version`

#### 请求

请求方式:`POST`

数据格式:`form-data`

发送数据:json格式的`localStorage`

`localStorage`中必须带的字段:`AcCookies`、`AcPassToken`

如果`header`返回了`set-cookie`字段下一次访问需要带上`cookie`

#### 返回

#####  正常

返回:`OK`

##### Cookie错误

不存在`AcCookies`和`AcPassToken`两个字段

返回:`Cookie Error`

##### 验证错误

上传的Cookie无法通过A站官方用户验证

返回:`Auth Error`

### 下载

接口:`/api/acfun-helper/options/download`

#### 请求

请求方式:`POST`

数据格式:`form-data`

发送数据:json格式的`localStorage`

`localStorage`中必须带的字段:`AcCookies`、`AcPassToken`

如果`header`返回了`set-cookie`字段下一次访问需要带上`cookie`

#### 返回

##### 正常

返回:json格式的`localStorage`

##### Cookie错误

不存在`AcCookies`和`AcPassToken`两个字段

返回:`Cookie Error`

##### 验证错误

上传的Cookie无法通过A站官方用户验证

返回:`Auth Error`