define(
    ['underscore', 'gettext', 'js/utils/date_utils', 'js/views/baseview', 'common/js/components/views/feedback_prompt',
     'common/js/components/views/feedback_notification'],
    function(_, gettext, DateUtils, BaseView, PromptView, NotificationView) {
        'use strict';

        var PreviousVideoUploadView = BaseView.extend({
            tagName: 'tr',

            events: {
                'click .remove-video-button.action-button': 'removeVideo'
            },

            initialize: function(options) {
                this.template = this.loadTemplate('previous-video-upload');
                this.videoHandlerUrl = options.videoHandlerUrl;
            },

            renderDuration: function(seconds) {
                var minutes = Math.floor(seconds / 60);
                var seconds = Math.floor(seconds - minutes * 60);

                return minutes + ':' + (seconds < 10 ? '0' : '') + seconds;
            },

            render: function() {
                var duration = this.model.get('duration');
                var renderedAttributes = {
                    // Translators: This is listed as the duration for a video
                    // that has not yet reached the point in its processing by
                    // the servers where its duration is determined.
                    duration: duration > 0 ? this.renderDuration(duration) : gettext('Pending'),
                    created: DateUtils.renderDate(this.model.get('created')),
                    status: this.model.get('status')
                };
                this.$el.html(
                    this.template(_.extend({}, this.model.attributes, renderedAttributes))
                );
                return this;
            },

            removeVideo: function(e) {
                // debugger;
                var video = this.model,
                    notification = new NotificationView.Mini({
                        title: gettext('Removing')
                    }),
                    videoView = this;

                if (e && e.preventDefault) {
                    e.preventDefault();
                }

                new PromptView.Warning({
                    title: gettext('Remove Video Confirmation'),
                    message: gettext('Are you sure you wish to remove this video. It cannot be reversed!'),
                    actions: {
                        primary: {
                            text: gettext('Remove'),
                            click: function(view) {
                                view.hide();
                                notification.show();
                                $.ajax({
                                    url: videoView.videoHandlerUrl + '/' + video.get('edx_video_id'),
                                    type: 'DELETE'
                                }).done(function() {
                                    notification.hide();
                                }).done(function() {
                                    videoView.remove();
                                });
                            }
                        },
                        secondary: {
                            text: gettext('Cancel'),
                            click: function(view) {
                                view.hide();
                            }
                        }
                    }
                }).show();
            }
        });

        return PreviousVideoUploadView;
    }
);
