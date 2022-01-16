import {makeStyles} from '@material-ui/core/styles';

export const useStyles = makeStyles((theme) => ({
  root: {
    padding: theme.spacing(1),
    border: `1px solid ${theme.palette.dark.blue['200']}`,
    borderRadius: '3px',
    width: '100%',
    display: 'flex',
    alignItems: 'center',
    gap: theme.spacing(2),
  },
  title: {
    fontSize: '16px',
    lineHeight: '16px',
    fontWeight: '600',
  },
  seenIcon: {
    color: theme.palette.primary.main,
    width: '15px',
    height: '15px',
  },
  content: {
    display: 'flex',
    flexDirection: 'column',
    justifyContent: 'center',
    gap: '0px',
  },
  secondary: {
    display: 'flex',
    alignItems: 'center',
    gap: '5px',
    opacity: '.8',
  },
}));