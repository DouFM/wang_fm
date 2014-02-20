/*
*   navigator controller
*/
function NavigatorCtrl($scope, $http, User) {
    angular.element(document).ready(function() {
        navInit();
    });
    
    $scope.login = function() {
        var postData = {
            arg: 'current/',
            name: 'admin',
            password: 'admin'
        };
        var loginInfo = User.login(postData, function(data) {
            var navBar = '<li><a href="#" onclick="logout()">退出</a></li><li>' + data.name + '</li>';
            $('#login').modal('hide');
            $('#navBar').html(navBar);
            $('#topPanel ul li').addClass('navLink');
            if(data.level === 'admin') {
                $('#navBar').append('<li><a href="#/manager">管理</a></li>');
            }
            console.info(data);
        });
    };

    // $scope.logout = function() {
    //     console.info('log out click!');
    // }

    function navInit() {
        $scope.currentUser = User.get({arg: 'current/'}, function(data) {
            $scope.data = data;
            if(data.name !== undefined) {
                var navBar = '<li><a href="#" onclick="logout()">退出</a></li><li>'
                            + data.name + '</li>';
                $('#navBar').html(navBar);
                $('#topPanel ul li').addClass('navLink');

                if(data.level === 'admin') {
                    $('#navBar').append('<li><a href="#/manager">管理</a></li>');
                }
            } else {
                var navBar = '<li><a href="#" data-toggle="modal">注册</a></li> \
                    <li><a href="#" data-target="#login" data-toggle="modal">登录</a></li>';
                $('#navBar').html(navBar);
            }
        });

        // console.info('navInit ready');
        console.info($scope.currentUser);
    }
}

function logout() {
    console.info('log out click!');
    $.ajax({
        type: 'delete',
        url: '/api/user/current/',
        success: function(data) {
            console.info('logout ' + data);
            window.location.href = '/static/app/views/index.html';
        }
    });
}

/*
*	channel controller
*/
function ChannelCtrl($scope, $http , Channel) {
    var channelList = Channel.query({start: 0});
    $scope.channels = channelList;
    //output bellow is []
    //console.info(channelList);
}


/*
*   musicplayer controller
*/
function MusicPlayerCtrl($scope, $http, Music) {
    angular.element(document).ready(function() {
        playInit();
        //console.log('Hello World');
    });

    function playInit() {
        new jPlayerPlaylist({
            jPlayer: "#jquery_jplayer_1",
            cssSelectorAncestor: "#jp_container_1"
        }, 
        [],
        { 
            ready: playReady,
            ended: playReady,
            swfPath: "/static/app/vender/jPlayer/js",
            supplied: "mp3",
            wmode: "window",
            smoothPlayBar: true,
            keyEnabled: true
        });

        $("#jp-report").html('<a href="#" data-toggle="tooltip" data-placement="top" title="请注册后使用!" alt="report" ><img src="../images/report.png"></img></a>');
        $("#jp-favorite").html('<a href="#" data-toggle="tooltip" data-placement="top" title="请注册后使用!" alt="favorite" o><img src="../images/favorite2.png"></img></a>');
        $("#jp-trash").html('<a href="#" data-toggle="tooltip" data-placement="top" title="请注册后使用!" alt="trash" ><img src="../images/trash2.png"></img></a>');      
    }

    function playReady() {
        //console.info('play ready');
        var musicList = Music.query({start: 0, end: 3}, function(data) {
            //console.info(data);
            $("#jquery_jplayer_1").jPlayer("setMedia", { mp3: data[0].audio }).jPlayer("load").jPlayer("play");
        });
        $scope.musics = musicList;
        //console.info(musicList);
    };


    function playEnded() {
        console.info('playEnded');
    };
}

/*
*   manager controller
*/
function managerCtrl($scope, $http, Music, Channel, User) {
    
    //music info display
    var musicList = Music.query({start: 0, end: 4});
    $scope.musics = musicList;

    // channel info display
    var channelNumAll = Channel.get();
    var channels = Channel.query({start: 0, end: 14});
    $scope.channelNumAll = channelNumAll;
    $scope.channels = channels;

    //user info display
    var currentUser = User.query({start: 0});
    $scope.users = currentUser;
}