// This java file will calculate the weekly average stuff from expo moving avg data

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.Statement;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Calendar;
import java.util.Date;
import java.util.List;

public class ArrivalWPSummary {
    public static Connection c = null;
    public static Statement stmt = null;
    public static void main(String[] args) throws Exception {
       openConnection();
       
       SimpleDateFormat formatter = new SimpleDateFormat("dd-MMM-yyyy");
       String sDateStr = "01-Jan-2006";
       String eDateStr = "26-Jun-2015";
       
       Date startDate;
       Date endDate;
       Calendar cal = Calendar.getInstance(); 
       
     /*  create table weekData(
sno SERIAL,
startDate Date,
endDate Date,
centreid Int,
arrival decimal,
wholesalePrice decimal,
retailprice decimal
)*/
       
       try {
            startDate = formatter.parse(sDateStr);
            endDate = formatter.parse(eDateStr);
            int centreid=44;
            cal.setTime(startDate);
            while(startDate.compareTo(endDate)<0)
            {
                Date sd=cal.getTime();
                cal.add(Calendar.DATE, 6);
                Date ed=cal.getTime();
                
                stmt = c.createStatement();
                String weekSelect ="select sum(arrivalsintons),avg(wholesaleprice),avg(retailprice) from expoAvgSmoothedData where centreid=? and dateofdata>=? and dateofdata<=?;";
                                
                PreparedStatement weekSelectPS = c.prepareStatement(weekSelect);
                weekSelectPS.setInt(1, centreid);
                weekSelectPS.setDate(2, new java.sql.Date(sd.getTime()));
                weekSelectPS.setDate(3, new java.sql.Date(ed.getTime()));
                ResultSet rs = weekSelectPS.executeQuery();
                
                while(rs.next())
                {
                    Statement insStmt =c.createStatement();
                    String insString="insert into weekData(startDate,endDate,centreid,arrival,wholesalePrice,retailprice) values(?,?,?,?,?,?)";
                    
                    PreparedStatement ps = c.prepareStatement(insString);
                    ps.setDate(1, new java.sql.Date(sd.getTime()));
                    ps.setDate(2, new java.sql.Date(ed.getTime()));
                    ps.setInt(3,centreid);
                    ps.setDouble(4,rs.getDouble(1) );
                    ps.setDouble(5,rs.getDouble(2) );
                    ps.setDouble(6,rs.getDouble(3) );
                    
                    ps.executeUpdate();
                    ps.close();
                }
                weekSelectPS.close();
                rs.close();
                
                cal.add(Calendar.DATE, 1);
                startDate= cal.getTime();
            }
       }
       catch(Exception e)
       { 
           System.err.println(""+e.getMessage());
       }
     
       
       
    }

    
    public static void openConnection() throws Exception
    {
        try {
         Class.forName("org.postgresql.Driver");
         c = DriverManager
            .getConnection("jdbc:postgresql://localhost:5432/onion",
            "postgres", "password");         
      }
      catch(Exception e)
      {
          System.err.println("Exception in commodityCode fetch "+e.getMessage());
          throw e;
      }
    }
    
}
