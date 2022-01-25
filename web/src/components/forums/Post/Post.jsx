import React from 'react';

import Box from '@material-ui/core/Box';
import Typography from '@material-ui/core/Typography';
import VisibilityIcon from '@material-ui/icons/Visibility';
import CommentIcon from '@material-ui/icons/Comment';
import CreateIcon from '@material-ui/icons/Create';

import Divider from '../../shared/Divider/Divider';
import CommentsList from '../CommentsList/CommentsList';
import {toRelativeDate} from '../../../utils/datetime';

import {useStyles} from './Post.styles';

export default function Post({
  title,
  content,
  user,
  seenCount,
  createdDate,
  updatedDate,
  comments,
}) {
  const classes = useStyles();

  return (
    <Box className={classes.root}>
      <Box className={classes.postInfoContainer}>
        <Box className={classes.profilePic}>
          <Typography>
            {user[0]}
          </Typography>
        </Box>
        <Typography className={classes.user}>
          {user}
        </Typography>
        <Typography className={classes.whenPosted}>
          posted on {toRelativeDate(new Date(createdDate))}
        </Typography>
      </Box>
      <Typography className={classes.title}>
        {title}
      </Typography>
      <Typography className={classes.content}>
        {content}
      </Typography>
      <Box className={classes.extraInfo}>
        <Box className={classes.infoContainer}>
          <VisibilityIcon className={classes.icon} />
          <Typography>
            {seenCount}
          </Typography>
        </Box>
        <Box className={classes.infoContainer}>
          <CommentIcon className={classes.icon} />
          <Typography>
            {comments.length}
          </Typography>
        </Box>
        <Box className={classes.infoContainer}>
          <CreateIcon className={classes.icon} />
          <Typography>
            {toRelativeDate(new Date(updatedDate))}
          </Typography>
        </Box>
      </Box>
      <Divider />
      <Box className={classes.commentListContainer}>
        <CommentsList comments={comments}/>
      </Box>
    </Box>
  );
};
