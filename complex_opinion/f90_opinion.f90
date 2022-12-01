include 'random_module.f90'   ! For using Random Number Generator

!----------------------------------------------------------------
module fpb
      use randomize
      implicit none

      ! For the random number generator.
      integer(4)                      :: idum
      integer                         :: ip, mm
      integer, dimension(8)           :: values

      integer(4), allocatable, dimension(:) :: de_begins
      integer(4), allocatable, dimension(:) :: de_sources
      integer(4), allocatable, dimension(:) :: de_targets
      real(4), allocatable, dimension(:)    :: states

      integer :: N , M
      real(8) :: H , T , p_1
      integer :: MC_step
contains
!-----------------------------------------------------------------
  subroutine init( seed )
      use randomize
      implicit none

      integer(4),intent( in ) :: seed

      ! Lets init the random number generator
      ! call date_and_time( VALUES = values )
      ! idum = ( values(8) + 100 ) * ( values(7) + 10 ) * 32168
      idum = seed     
      mm  = mzranset( 521288629 , 362436069 , 16163801 , idum )

      MC_step = 0
      N = size( de_begins ) - 1
      M = size( de_sources ) / 2

  end subroutine

  subroutine finish()
      implicit none
   
  end subroutine
!-----------------------------------------------------------------
!  function degree( i )
!      implicit none

!      integer :: degree
!      integer,intent( in ) :: i

!      if ( i .lt. 1 ) then
!          print *, "f90.ERROR @ degree(...) : i < 1."
!      end if
!      if ( i .gt. N ) then
!          print *, "f90.ERROR @ degree(...) : i > N."
!      end if

!      degree = de_begins( i + 1 ) - de_begins( i )
!  end function
!-----------------------------------------------------------------
  function de_ends( i )
      implicit none
      integer :: de_ends
      integer,intent( in ) :: i
      de_ends = de_begins( i + 1 ) - 1
  end function
!-----------------------------------------------------------------
  subroutine set_parameters_opinion_dynamics( param_H , param_T , param_p_1 )
      real(8),intent( in ) :: param_H
      real(8),intent( in ) :: param_T
      real(8),intent( in ) :: param_p_1

      H = param_H
      T = param_T
      p_1  = param_p_1
  end subroutine
!-----------------------------------------------------------------
  function num_actives_1()
     implicit none
     integer :: num_actives_1
     integer :: i
     num_actives_1 = 0
     do i = 1 , N
         if ( states( i ) .eq. 1 ) then
            num_actives_1 = num_actives_1 + 1
         end if
     end do
  end function

!-----------------------------------------------------------------
  function num_actives_0()
     implicit none
     integer :: num_actives_0
     integer :: i
     num_actives_0 = 0
     do i = 1 , N
         if ( states( i ) .eq. 0 ) then
            num_actives_0 = num_actives_0 + 1
         end if
     end do
  end function
!-----------------------------------------------------------------
  function opinion_dynamics( num_MC_steps )
      use randomize
      implicit none

      integer,intent( in ) :: num_MC_steps
      integer(4) :: step, i, j
      integer  :: l
      real(8)  :: q, exponencial, xlambda1, p_2
      real(8)  :: M_tot_step
      real(8), dimension(num_MC_steps)    :: p2_vs_s_sim
      real(8), dimension(num_MC_steps)    :: opinion_dynamics


      M_tot_step = 0.d0
      p2_vs_s_sim = 0.d0


      ! state_i == 1 >>>> up
      ! state_i == 0 >>>> down

      do MC_step = 1 , num_MC_steps ! MC_step es mct (monte carlo time)
         do step = 1 , N

            i = int( random() * N ) + 1
            ! we select a node
            l = int( random() * ( (de_ends( i ) - de_begins( i )) + 1) )
            ! random number times the degree of the selected node
            j = de_targets( de_begins( i ) + l )
            ! we select one of the neighbors of the selected node

            !print *, "step=" , step, "i =" , i , "j =" , j , "s(i) =" , states( i ), "s(j) =" , states( j )
         
            ! with probability p_1 node i mimics the state of node j
            if ( random() .le. p_1 ) then
             states( i ) = states ( j )
            endif
         
         ! change states to +-1 to calculate magnetization
         if ( states(i) .eq. 1 ) then
             q = 1  
         else
             q = -1
         endif

         exponencial = exp( ( 1.0 + q*H) / T )
         xlambda1 = exponencial + 1.0 / exponencial
         p_2 = exponencial / xlambda1
    
!if(T .eq. 0.0) then
!p_2=1.d0
!else

         if ( random() .gt. p_2 ) then
             if( states( i ) .eq. 1 ) then 
                 states( i ) = 0
             else  
                 states( i ) = 1
             end if
         else
             states( i ) = states( i )
         end if 
          
         if ( i .lt. 1 ) then
              print *,"ERROR @ opinion_dynamics : i =" , i , " < 1"
              stop         
         end if
         if ( i .gt. N ) then
              print *,"ERROR @ opinion_dynamics : i =" , i , " > N"
              stop         
         end if
 
         end do ! step of actualization of N nodes

         ! acá puedo agregar un write de la magnetización actual
         ! del sistema, para tener la evolución temporal del
         ! sistema al final del loop.
         ! Problema: notar que los datos se están extrayendo a
         ! python via num_actives y no mediante un return o un
         ! write acá.

         M_tot_step = (num_actives_1() - num_actives_0()) / real(N)
         p2_vs_s_sim(MC_step) = M_tot_step

      end do ! MC_step

      opinion_dynamics = p2_vs_s_sim

end function
!-----------------------------------------------------------------
  function get_MC_steps()
      implicit none
      integer :: get_MC_steps
      get_MC_steps = MC_step
  end function

  function get_N()
      implicit none
      integer :: get_N
      get_N = N
  end function

  function get_M()
      implicit none
      integer :: get_M
      get_M = M
  end function

end module fpb