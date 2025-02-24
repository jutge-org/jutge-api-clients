import java.io.FileOutputStream;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.stream.Collectors;

/**
 * This is a tutorial script that shows how to use the Jutge API client in Java.
 *
 * Full reference documentation is available at https://api.jutge.org
 */
public class Tutorial {

    public static void main(String[] args) throws Exception {
        // Create a Jutge API client
        JutgeApiClient jutge = new JutgeApiClient();

        // Get a fortune cookie
        System.out.println(jutge.misc.getFortune());

        // Get the current time in the server and print one of its attributes
        JutgeApiClient.Time time = jutge.misc.getTime();
        System.out.println(time.full_time);
        System.out.println();

        // Get the homepage stats and print them
        var stats = jutge.misc.getHomepageStats();
        System.out.printf("users: %d, problems: %d, submissions: %d%n", stats.users, stats.problems, stats.submissions);
        System.out.println();

        // Download the Jutge logo, save it to a file and show it in the browser
        var logo = jutge.misc.getLogo();
        FileOutputStream fos = new FileOutputStream("logo.png");
        fos.write(logo.data);
        fos.close();

        // Get all compilers and print their name for those that are C++
        var compilers = jutge.tables.getCompilers();
        for (var entry : compilers.entrySet()) {
            String compilerId = entry.getKey();
            var compiler = entry.getValue();
            if (compiler.language == "C++") {
                System.out.printf("%s: '%s' (%s)%n", compilerId, compiler.name, compiler.language);
            }
        }
        System.out.println();

        // Get P68688 (Hello, world!) problem and print its title, author and English
        // statement.
        /*
         * var problem = jutge.problems.getProblem("P68688_en");
         * System.out.println(problem.title);
         * System.out.println(problem.abstract_problem.author);
         * String statement = jutge.problems.getTextStatement("P68688_en");
         * System.out.println(statement);
         * System.out.println();
         */

        // All previous functions where public, but in order to access
        // other functions, we need to login using Jutge.org credentials.
        String email = "jpetit@cs.upc.edu";
        String password = "finsalscollonsOO";
        jutge.login(email, password);

        // Get user's name and uid in the profile.
        var profile = jutge.student.profile.get();
        System.out.println(profile.name);
        System.out.println(profile.user_uid);
        System.out.println();

        // All authenticated users are students and can use the student module.
        // There are other modules for different roles, such as admin, instructor, etc.

        // Get all problem statuses, filter those that are accepted and print the first
        // 8 in alphabetical order.
        var statuses = jutge.student.statuses.getAll();
        List<String> accepteds = new ArrayList<>();
        for (var entry : statuses.entrySet()) {
            String problemNm = entry.getKey();
            var status = entry.getValue();
            if ("accepted".equals(status.status)) {
                accepteds.add(problemNm);
            }
        }
        Collections.sort(accepteds);
        List<String> first8 = accepteds.stream().limit(8).collect(Collectors.toList());
        System.out.println(first8);
        System.out.println();

        // Get the status of P68688
        /*
         * var status = jutge.student.statuses.getForAbstractProblem("P68688");
         * System.out.println(status);
         * System.out.println();
         */

        // Logout is optional, but recommended.
        jutge.logout();
    }
}
