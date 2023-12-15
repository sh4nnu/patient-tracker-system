import React, { useState, useEffect, useContext } from 'react';
import classes from './AppointmentList.module.css';
import Appointment from './Appointment';
import config from '../../config.json';
import AuthContext from '../../store/auth-context';

function AppointmentList() {
    const [todaysAppointments, setTodaysAppointments] = useState([]);
    const [upcomingAppointments, setUpcomingAppointments] = useState([]);
    const [doctorOptions, setDoctorOptions] = useState([]); // To store doctor options
    const authCtx = useContext(AuthContext);


    useEffect(() => {
        // Function to fetch appointments
        const fetchAppointments = (date) => {
            var myHeaders = new Headers();
            myHeaders.append("Accept", "application/json");
            // Replace this cookie value with the actual session cookie from authentication
            myHeaders.append("Cookie", "session=YOUR_SESSION_COOKIE");

            var requestOptions = {
                method: 'GET',
                headers: myHeaders,
                redirect: 'follow'
            };

            // Use the date parameter to fetch either today's appointments or all appointments
            const baseUrl = `http://${config.ipAddress}:${config.port}/patients/${authCtx.user.roleId}/appointments`;
            const url = date ? `${baseUrl}?date=${date}` : baseUrl;

            fetch(url, requestOptions)
                .then(response => response.json())
                .then(result => {
                    const appointments = result.data; // Adjust this according to the actual result structure
                    const now = new Date();
                    const today = now.toISOString().split('T')[0];
                    console.log("appointment page: today " + today);
                    console.log(appointments);
                    // Filter today's appointments
                    const todayAppointments = appointments.filter(a => a.date === today);

                    // Filter upcoming appointments
                    const upcomingAppointments = appointments.filter(a => {
                        const appointmentDate = new Date(`${a.date} ${a.end_time}`);
                        return appointmentDate > now && a.date !== today;
                    });

                    setTodaysAppointments(todayAppointments);
                    setUpcomingAppointments(upcomingAppointments);
                })
                .catch(error => console.log('error', error));
        };

        // Fetch today's appointments
        const today = new Date().toISOString().split('T')[0];
        fetchAppointments(today);
        // Fetch all upcoming appointments
        fetchAppointments();
        // Fetch doctors and store them in doctorOptions
        const fetchDoctors = async () => {
            try {
                var myHeaders = new Headers();
                myHeaders.append("Content-Type", "application/json");
                myHeaders.append("Cookie", `session=${authCtx.session}`);

                var requestOptions = {
                    method: 'GET',
                    headers: myHeaders,
                    redirect: 'follow'
                };

                const response = await fetch(`http://${config.ipAddress}:${config.port}/doctors`, requestOptions);
                const data = await response.json();

                const doctorOptions = data.data.map(doctor => ({
                    value: doctor.doctor_id,
                    label: doctor.full_name
                }));
                setDoctorOptions(doctorOptions);
            } catch (error) {
                console.log('error', error);
            }
        };

        fetchDoctors();
    }, [authCtx.session]);

    // Function to get doctor name based on doctor ID
    const getDoctorName = (doctorId) => {
        const selectedDoctor = doctorOptions.find(doctor => doctor.value === doctorId);
        return selectedDoctor ? selectedDoctor.label : 'Unknown Doctor';
    };

    // Function to get patient name based on authCtx
    const getPatientName = () => {
        return `${authCtx.user.firstName} ${authCtx.user.lastName}`;
    };

    return (
        <ul className={classes.list}>
            {todaysAppointments.length > 0 && (
                <>
                    <h2>Today's Appointments</h2>
                    {todaysAppointments.map((appointment) => (
                        <Appointment
                            key={appointment.id}
                            id={appointment.id}
                            title={appointment.title}
                            patientName={getPatientName()}
                            doctorName={getDoctorName(appointment.doctor_id)}
                            datetime={appointment.date}
                            start_time={appointment.start_time}
                            end_time={appointment.end_time}
                        />
                    ))}
                </>
            )}

            {upcomingAppointments.length > 0 ? (
                <>
                    <h2>Upcoming Appointments</h2>
                    {upcomingAppointments.map((appointment) => (
                        <Appointment
                            key={appointment.id}
                            id={appointment.id}
                            title={appointment.title}
                            patientName={getPatientName()}
                            doctorName={getDoctorName(appointment.doctor_id)}
                            datetime={appointment.date}
                            start_time={appointment.start_time}
                            end_time={appointment.end_time}
                        />
                    ))}
                </>
            ) : (
                <div className={classes.noAppointmentsCard}>No upcoming appointments...</div>
            )}

            {todaysAppointments.length === 0 && upcomingAppointments.length === 0 && (
                <div className={classes.noAppointmentsCard}>No appointments for today or in the future...</div>
            )}
        </ul>
    );
}

export default AppointmentList;
