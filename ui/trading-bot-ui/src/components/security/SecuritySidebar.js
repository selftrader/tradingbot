import { Box, List, ListItemButton, ListItemText } from "@mui/material";

const navItems = [
  { id: "overview", label: "Overview" },
  { id: "certifications", label: "Certifications" },
  { id: "infrastructure", label: "Infrastructure Security" },
  { id: "compliance", label: "Compliance Contact" },
];

const SecuritySidebar = ({ active, onNavigate }) => (
  <Box sx={{ minWidth: 200, pr: 4 }}>
    <List dense>
      {navItems.map((item) => (
        <ListItemButton
          key={item.id}
          selected={active === item.id}
          onClick={() => onNavigate(item.id)}
        >
          <ListItemText primary={item.label} />
        </ListItemButton>
      ))}
    </List>
  </Box>
);

export default SecuritySidebar;
